from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.forms.evaluation_forms import AssessmentForm
from backend.models.evaluations import Assessment
from backend.models.gestion_ecole import AcademicYear, ClassRoom, Series, Student, StudentClassroom, Subject
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

def calcul_moyenne_college(notes_devoirs, notes_compos):
    # Vérification si les listes des notes de devoirs et de compositions ont la même longueur
    if len(notes_devoirs) != len(notes_compos):
        raise ValueError("Les listes des notes de devoirs et de compositions doivent avoir la même longueur")
    
    # Calcul de la moyenne de chaque matière
    moyennes_matieres = []
    for note_devoir, note_compo in zip(notes_devoirs, notes_compos):
        moyenne_matiere = round((note_devoir + note_compo) / 2, 2)
        print(moyenne_matiere)
        moyennes_matieres.append(moyenne_matiere)
    
    # Calcul de la moyenne du trimestre (moyenne générale de toutes les matières)
    moyenne_trimestre = round(sum(moyennes_matieres) / len(moyennes_matieres), 2)
    
    return moyenne_trimestre


def calcul_resultat_primaire(period, classroom, student, academic_year):
    evaluations = Assessment.objects.filter(
        period=period, 
        classroom=classroom, 
        academic_year=academic_year, 
        student=student,
    )

    # Extraire les notes à partir des évaluations
    notes = [evaluation.note_exam for evaluation in evaluations]

    average = moyenne_primaire(notes)
    student_career = StudentClassroom.objects.get(classroom=classroom, student=student, academic_year=academic_year, is_next=False)
    
    return {
        'id_student':student_career.student.id,
        'nui':student_career.student.registration_number,
        'lastname':student_career.student.lastname,
        'firstname':student_career.student.firstname,
        'classroom':student_career.classroom.title,
        'type':student_career.classroom.types,
        'average':average,
        'period':period,
    }


def calcul_resultat_college(period, classroom, student, academic_year):
    try:
        evaluations = Assessment.objects.filter(
            period=period, 
            classroom=classroom, 
            academic_year=academic_year, 
            student=student,
        )

        moyennes_matieres = []
        for evaluation in evaluations:
            moyenne_matiere = round((evaluation.note + evaluation.note_exam) / 2, 2)
            print(moyenne_matiere)
            moyennes_matieres.append(moyenne_matiere)
            
        average = round(sum(moyennes_matieres) / len(moyennes_matieres), 2)
        
        student_career = StudentClassroom.objects.get(classroom=classroom, student=student, academic_year=academic_year, is_next=False)
        
        return {
            'id_student':student_career.student.id,
            'nui':student_career.student.registration_number,
            'lastname':student_career.student.lastname,
            'firstname':student_career.student.firstname,
            'classroom':student_career.classroom.title,
            'type':student_career.classroom.types,
            'average':average,
            'period':period,
        }
    except (Assessment.DoesNotExist, StudentClassroom.DoesNotExist):
        return[]


def get_all_results(academic_year):
    results = []
    try:
        students_classrooms = StudentClassroom.objects.filter(academic_year=academic_year, is_registered=True, is_next=False)

        for student_classroom in students_classrooms:
            if student_classroom.classroom.types == 'Primaire':
                results.append(calcul_resultat_primaire(
                    period='Octobre',
                    classroom=student_classroom.classroom,
                    student=student_classroom.student,
                    academic_year=academic_year
                ))
            else:
                pass
            
        results = sorted(results, key=lambda x: x['average'], reverse=True)
        return results;
    except StudentClassroom.DoesNotExist:
        return results
    
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
        classrooms = ClassRoom.objects.filter(level__school=request.user.school)
        subjects = Subject.objects.filter(level__school=request.user.school)
        student_ids = StudentClassroom.objects.filter(academic_year__school=request.user.school, academic_year__status=True).values_list('student', flat=True).distinct()
        students = Student.objects.filter(id__in=student_ids)
        context = {
            'form': form,
            'classrooms':classrooms,
            'subjects':subjects,
            'students':students,
            'evaluation':evaluation
        }
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
        classrooms = ClassRoom.objects.filter(level__school=request.user.school)
        subjects = Subject.objects.filter(level__school=request.user.school)
        student_ids = StudentClassroom.objects.filter(academic_year__school=request.user.school, academic_year__status=True).values_list('student', flat=True).distinct()
        students = Student.objects.filter(id__in=student_ids)
        context = {
            'form': form,
            'classrooms':classrooms,
            'subjects':subjects,
            'students':students
        }
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

            evaluations = Assessment.objects.filter(classroom=classroom, subject=subject, period=request.POST['period']).order_by('-note', '-note_exam')

            classrooms = ClassRoom.objects.filter(level__school=request.user.school)
            subjects = Subject.objects.filter(level__school=request.user.school)
            
            if evaluations.exists():
                if evaluations.first().note > evaluations.first().note_exam:
                    max_note = evaluations.first().note
                    last_note = evaluations.last().note_exam
                else:
                    max_note = evaluations.first().note_exam
                    last_note = evaluations.last().note
                
                count = evaluations.count()
                # Calcul de la somme des notes de devoirs et des notes d'examens à partir de la base de données
                sum_notes_devoirs = evaluations.aggregate(total=Sum('note'))['total']
                sum_notes_examens = evaluations.aggregate(total=Sum('note_exam'))['total']

                # Calcul de la moyenne en ajoutant les deux sommes et en divisant par 2
                sum_notes = round((sum_notes_devoirs + sum_notes_examens) / 2, 2)
                
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
        student_career = StudentClassroom.objects.get(academic_year=academic_year)
        total_student = StudentClassroom.objects.filter(academic_year=academic_year).count()
        evaluations = Assessment.objects.filter(academic_year=academic_year).order_by('subject__label')
        subjects = []
        result = {}
        
        

        #qr_code_data = f"Matricule:{student_career.student.registration_number}\nParcours:{student_career.career.title}\Semestre:{student_career.semester.title}\\Niveau:{student_career.semester.level.label}\\Moyenne:{result['average']}\\Annee-academique:{academic_year.label}\nEtablissement:"
        filename = f"qr_code_{student_career.student.registration_number}.png"  # Nom du fichier pour l'image du code QR

        # Générer le code QR et enregistrer l'image
        #qr_code_path = generate_qr_code_and_save(qr_code_data, filename)
        context = {
            'student_career': student_career,
            'year': academic_year,
            'result': result,
            'subjects': subjects,
            'total_student': total_student,
            #'qr_code_path': qr_code_path
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

