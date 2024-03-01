from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.forms.evaluation_forms import AssessmentForm
from backend.models.evaluations import Assessment
from backend.models.gestion_ecole import AcademicYear, ClassRoom, Series, StudentClassroom, Subject
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from elimu_school.constant import generate_qr_code_and_save

# Fonction pour calculer la moyenne au primaire
def moyenne_primaire(notes):
    somme_notes = sum(notes)
    nombre_matières = len(notes)
    moyenne = somme_notes / nombre_matières
    return moyenne

# Fonction pour calculer la moyenne au collège
def moyenne_college_lycee(notes, notes_exam, coefficients):
    somme_notes_ponderees = sum(note + ( note_exam * coeff) for note, note_exam, coeff in zip(notes, notes_exam, coefficients))
    somme_coefficients = sum(coefficients)
    moyenne = somme_notes_ponderees / somme_coefficients
    return moyenne


def calcul_resultat_primaire(period, classroom_id, user, student):
    try:
        academic_year = AcademicYear.objects.get(status=True, school=user.school)
        classroom = ClassRoom.objects.get(pk=classroom_id)
        evaluations = Assessment.objects.filter(
            period=period, 
            classroom=classroom, 
            academic_year=academic_year, 
            student=student,
            type_evaluation='Examen'
        )

        # Extraire les notes à partir des évaluations
        notes = [evaluation.note for evaluation in evaluations]

        average = moyenne_primaire(notes)
        student_career = StudentClassroom.objects.get(classroom=classroom, student=student, academic_year=academic_year, is_next=False)
        
        return {
            'nui':student_career.student.registration_number,
            'lastname':student_career.student.lastname,
            'firstname':student_career.student.firstname,
            'classroom':student_career.classroom.title,
            'average':average,
            'period':period,
        }
    except (AcademicYear.DoesNotExist, ClassRoom.DoesNotExist, StudentClassroom.DoesNotExist):
        return[]


def calcul_resultat_college_lycee(period, classroom_id, user, student):
    try:
        academic_year = AcademicYear.objects.get(status=True, school=user.school)
        classroom = ClassRoom.objects.get(pk=classroom_id)
        evaluations_examens = Assessment.objects.filter(
            period=period, 
            classroom=classroom, 
            academic_year=academic_year, 
            student=student,
            type_evaluation='Examen'
        )
        
        evaluations = Assessment.objects.filter(
            period=period, 
            classroom=classroom, 
            academic_year=academic_year, 
            student=student,
            type_evaluation='Devoir de classe'
        )

        # Extraire les notes à partir des évaluations
        notes = [evaluation.note for evaluation in evaluations]
        notes_exam = [evaluation.note for evaluation in evaluations_examens]
        coefficiens = [evaluation.subject.coefficient for evaluation in evaluations]

        average = moyenne_college_lycee(notes, notes_exam, coefficiens)
        student_career = StudentClassroom.objects.get(classroom=classroom, student=student, academic_year=academic_year, is_next=False)
        
        return {
            'nui':student_career.student.registration_number,
            'lastname':student_career.student.lastname,
            'firstname':student_career.student.firstname,
            'classroom':student_career.classroom.title,
            'average':average,
        }
    except (AcademicYear.DoesNotExist, ClassRoom.DoesNotExist, StudentClassroom.DoesNotExist):
        return[]

class EditAssessmentView(View):
    template = 'manager_dashboard/evaluations/editer_evaluation.html'
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('manager_dashboard:no_year')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, pk, *args, **kwargs):
        evaluation = get_object_or_404(Assessment, pk=pk)
        form = AssessmentForm(request.user, instance=evaluation)
        context = {'form': form}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        evaluation = get_object_or_404(Assessment, pk=pk)
        year = get_object_or_404(AcademicYear, status=True, school=request.user.school)
        mutable_data = request.POST.copy()
        mutable_data['academic_year'] = year
        form = AssessmentForm(request.user, mutable_data, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, "Evaluation a été modifier avec succès")
            return redirect('manager_dashboard:evaluations')
        else:
            print(form.errors)
        messages.error(request, "ERREUR: Impossible de modifier l'évaluation")
        context = {'form':form}
        return render(request, template_name=self.template, context=context)

class AddAssessmentView(View):
    template = 'manager_dashboard/evaluations/ajout_evaluation.html'
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('manager_dashboard:no_year')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        form = AssessmentForm(request.user)
        context = {'form': form}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, *args, **kwargs):
        year = get_object_or_404(AcademicYear, status=True, school=request.user.school)
        mutable_data = request.POST.copy()
        mutable_data['academic_year'] = year
        form = AssessmentForm(request.user, mutable_data)
        if form.is_valid():
            form.save()
            messages.success(request, "Évaluation a été enregistré avec succès")
            return redirect('manager_dashboard:evaluations')
        
        messages.error(request, "ERREUR: Impossible d'enregistré l'évaluarion")
        context = {'form':form}
        return render(request, template_name=self.template, context=context)
    
class AssessmentView(View):
    template = 'manager_dashboard/evaluations/evaluations.html'
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('manager_dashboard:no_year')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        year = AcademicYear.objects.get(status=True, school=request.user.school)
        evaluations = Assessment.objects.filter(academic_year=year).order_by('-created_at')
        # Nombre d'éléments par page
        items_per_page = 7
        
        paginator = Paginator(evaluations, items_per_page)
        
        page = request.GET.get('page')
        
        try:
            # Obtenez les éléments de la page demandée
            data_page = paginator.page(page)
        except PageNotAnInteger:
            # Si la page n'est pas un entier, affichez la première page
            data_page = paginator.page(1)
        except EmptyPage:
            # Si la page est en dehors de la plage, affichez la dernière page
            data_page = paginator.page(paginator.num_pages)
            
        context = {'evaluations': data_page}
        
        return render(request, template_name=self.template, context=context)
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Assessment, pk=pk)
        instance.delete()
        evaluations = Assessment.objects.filter(academic_year__school=request.user.school).order_by('-created_at')
        context = {'evaluations': evaluations}
        return render(request, template_name=self.template, context=context)

class NoteTableView(View):
    template = 'manager_dashboard/evaluations/tableau_notes.html'
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('manager_dashboard:no_year')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        classrooms = ClassRoom.objects.filter(level__school=request.user.school)
        subjects = Subject.objects.filter(level__school=request.user.school)
        context = {
            'classrooms':classrooms,
            'subjects':subjects
        }
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, *args, **kwargs):
        classroom_id = request.POST['classroom']
        subject_id = request.POST['subject']
        
        try:
            classroom = ClassRoom.objects.get(pk=classroom_id)
            subject = Subject.objects.get(pk=subject_id)

            evaluations = Assessment.objects.filter(classroom=classroom, subject=subject, period=request.POST['period']).order_by('-note')

            classrooms = ClassRoom.objects.filter(level__school=request.user.school)
            subjects = Subject.objects.filter(level__school=request.user.school)
            
            if evaluations.exists():
                max_note = evaluations.first().note
                last_note = evaluations.last().note
                count = evaluations.count()
                sum_notes = evaluations.aggregate(total=Sum('note'))['total']
                average = sum_notes / count if count > 0 else 0

                
                context = {
                    'classrooms':classrooms,
                    'subjects':subjects,
                    'evaluations':evaluations,
                    'max_note':max_note,
                    'last_note':last_note,
                    'average':average
                }
                return render(request, template_name=self.template, context=context)
            else:
                context = {
                    'classrooms':classrooms,
                    'subjects':subjects,
                    'subjects':subjects,
                }
                return render(request, template_name=self.template, context=context)

        except (Series.DoesNotExist, ClassRoom.DoesNotExist, Subject.DoesNotExist) as e:
            return HttpResponse(f"Erreur: {e}")

    
class AverageTableView(View):
    template = 'manager_dashboard/evaluations/tableau_moyennes.html'

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('manager_dashboard:no_year')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        classrooms = ClassRoom.objects.filter(level__school=request.user.school)
        subjects = Subject.objects.filter(level__school=request.user.school)
        context = {
            'classrooms':classrooms,
            'subjects':subjects
        }
        return render(request, template_name=self.template, context=context)
    

class BulletinDetailView(View):
    template_name = 'manager_dashboard/evaluations/bulletin_detail.html'
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('manager_dashboard:no_year')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get_context_data(self, request, pk, *args, **kwargs):
        academic_year = AcademicYear.objects.get(status=True, school=request.user.school)
        student_career = StudentClassroom.objects.get(pk=pk, academic_year=academic_year)
        total_student = StudentClassroom.objects.filter(semester=student_career.semester, career=student_career.career, academic_year=academic_year).count()
        evaluations = Assessment.objects.filter(semester=student_career.semester, career=student_career.career, academic_year=academic_year).order_by('subject__label')
        subjects = []
        result = {}
        
        if evaluations.exists():
            controle_evaluations = evaluations.filter(type_evaluation__title='Contrôle')
            partiel_evaluations = evaluations.filter(type_evaluation__title='Partiel')
            count_coefficient = 0

            for controle_evaluation in controle_evaluations.filter(student=student_career.student):
                count_coefficient += controle_evaluation.subject.coefficient
                partiel_evaluation = partiel_evaluations.filter(
                    student=controle_evaluation.student,
                    subject=controle_evaluation.subject
                ).first()

                if partiel_evaluation:
                    total = ((controle_evaluation.note + partiel_evaluation.note) * controle_evaluation.subject.coefficient) / 2
                    subjects.append(
                        {
                            'nui': controle_evaluation.student.registration_number,
                            'controle': controle_evaluation.note,
                            'partiel': partiel_evaluation.note,
                            'label': controle_evaluation.subject.label,
                            'coefficient': controle_evaluation.subject.coefficient,
                            'total': total,
                        }
                    )

            # Calculer la moyenne pondérée
            average = round(sum(x['total'] for x in subjects) / count_coefficient, 2) if count_coefficient != 0 else 0
            total_general = round(sum(x['total'] for x in subjects), 2)

            result = {
                'nui': subjects[0]['nui'] if subjects else '',
                'average': average,
                'count_coefficient': count_coefficient,
                'total_general': total_general
            }

        qr_code_data = f"Matricule:{student_career.student.registration_number}\nParcours:{student_career.career.title}\Semestre:{student_career.semester.title}\\Niveau:{student_career.semester.level.label}\\Moyenne:{result['average']}\\Annee-academique:{academic_year.label}\nEtablissement:"
        filename = f"qr_code_{student_career.student.registration_number}.png"  # Nom du fichier pour l'image du code QR

        # Générer le code QR et enregistrer l'image
        qr_code_path = generate_qr_code_and_save(qr_code_data, filename)
        context = {
            'student_career': student_career,
            'year': academic_year,
            'result': result,
            'subjects': subjects,
            'total_student': total_student,
            'qr_code_path': qr_code_path
        }
        return context
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = self.get_context_data(request, pk)
        return render(request, template_name=self.template_name, context=context)
    
    def check(self, pk, *args, **kwargs):
        student_career = get_object_or_404(StudentClassroom, pk=pk)
        student_career.is_registered = True
        student_career.is_valid = True;
        student_career.save()
        return redirect('manager_dashboard:academic_result')

