from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.forms.evaluation_forms import ReportCardForm
from backend.models.evaluations import ReportCard
from backend.models.gestion_ecole import AcademicYear, ClassRoom, Series, StudentClassroom
from django.http import Http404, JsonResponse
from django.contrib import messages

class NotAcademicYearFound(View):
    template_name = "manager_dashboard/statistique/no_academique.html"
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

class CloseAcademicYear(View):
    
    def get(self, request, *args, **kwargs):
        year = AcademicYear.objects.get(status=True, school=request.user.school)
        year.status = False
        year.save()
        del request.session['academic_year']
        return redirect('manager_dashboard:years')

class ResultatAcademique(View):
    template_name = "manager_dashboard/statistique/resultat_academique.html"
    
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
        
    
    def get_context_data(self, request, **kwargs):
        semesters = Series.objects.filter(level__school=self.request.user.school)
        careers = ClassRoom.objects.filter(sector__school=self.request.user.school)
        academic_year = AcademicYear.objects.filter(status=True, school=self.request.user.school).first()
        total_student = StudentClassroom.objects.filter(academic_year=academic_year, is_next=False).count()
        results = get_all_results(request.user)
        admis, echouer = 0, 0
        
        for i in results:
            if i['average'] >= 10:
                admis += 1
            else:
                echouer += 1
        context = {
            'academic_year': academic_year, 
            'results': results, 
            'semesters': semesters, 
            'careers': careers,
            'total_student': total_student,
            'admis': admis,
            'echouer': echouer
        }
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        semester_id = request.POST.get('semester')
        career_id = request.POST.get('career')
        try:
            career = ClassRoom.objects.get(pk=career_id)
            semester = Series.objects.get(pk=semester_id)
        except (ClassRoom.DoesNotExist, Series.DoesNotExist):
            raise Http404("Selected semester or career does not exist.")
        
        context = self.get_context_data(request)
        results = calculate_results(semester_id=semester_id, career_id=career_id, user=request.user)
        
        context.update({
            'career': career,
            'semester': semester,
            'results':results
        })
        return render(request, template_name=self.template_name, context=context)

class EditReportCardView(View):
    template = 'manager_dashboard/statistique/editer_bulletin.html'
    
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
        evaluation = get_object_or_404(ReportCard, pk=pk)
        form = ReportCardForm(request.user, instance=evaluation)
        context = {'form': form}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        evaluation = get_object_or_404(ReportCard, pk=pk)
        year = get_object_or_404(AcademicYear, status=True, school=request.user.school)
        mutable_data = request.POST.copy()
        mutable_data['academic_year'] = year
        mutable_files = request.FILES.copy()
        if 'file' not in mutable_files or not mutable_files['file']:
            mutable_files['file'] = None
            
        form = ReportCardForm(request.user, mutable_data, mutable_files, instance=evaluation)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Bulletin modifier avec succès")
            return redirect('manager_dashboard:bulletins')
        
        messages.error(request, "ERREUR: Impossible de modifier un bulletins")
        context = {'form':form}
        return render(request, template_name=self.template, context=context)

class AddReportCardView(View):
    template = 'manager_dashboard/statistique/ajouter_bulletin.html'
    
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
        form = ReportCardForm(request.user)
        context = {'form': form}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, *args, **kwargs):
        year = get_object_or_404(AcademicYear, status=True, school=request.user.school)
        mutable_data = request.POST.copy()
        mutable_data['academic_year'] = year
        form = ReportCardForm(request.user, mutable_data, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Bulletin enregister avec succès")
            return redirect('manager_dashboard:bulletins')
        
        messages.error(request, "ERREUR: Impossible d'ajouter un bulletins")
        context = {'form':form}
        return render(request, template_name=self.template, context=context)
    
class ReportCardView(View):
    template = 'manager_dashboard/statistique/bulletins.html'
    
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
        results = ReportCard.objects.filter(academic_year=year).order_by('-created_at')
        semesters = Series.objects.filter(level__school=request.user.school)
        careers = ClassRoom.objects.filter(sector__school=request.user.school)
        
        context = {
            'semesters': semesters,
            'careers': careers,
            'results': results
        }
        
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, *args, **kwargs):
        year = AcademicYear.objects.get(status=True, school=request.user.school)
        semester_id = request.POST['semester']
        career_id = request.POST['career']

        results = ReportCard.objects.filter(semester__id=semester_id, career__id=career_id, academic_year=year)
        
        semesters = Series.objects.filter(level__school=request.user.school)
        careers = ClassRoom.objects.filter(sector__school=request.user.school)
        
        if results:
            context = {
                'semesters': semesters,
                'careers': careers,
                'results': results,
            }
        else:
            context = {
                'semesters': semesters,
                'careers': careers,
            }

        return render(request, template_name=self.template, context=context)
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(ReportCard, pk=pk)
        instance.delete()
        return JsonResponse({'message': 'Élément supprimé avec succès'})

class NextLevelView(View):
    template_name = "manager_dashboard/statistique/monter_niveau.html"
    
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
    
    def get_context_data(self, request, **kwargs):
        semesters = Series.objects.filter(level__school=self.request.user.school)
        careers = ClassRoom.objects.filter(sector__school=self.request.user.school)
        academic_year = AcademicYear.objects.filter(status=True, school=self.request.user.school).first()
        
        student_validated = StudentClassroom.objects.filter(is_valid=True, is_registered=True, is_next=False, academic_year=academic_year)
        context = {
            'academic_year': academic_year, 
            'student_validated': student_validated, 
            'semesters': semesters, 
            'careers': careers,
        }
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, template_name=self.template_name, context=context)
    
    def unChecked(self, pk, *args, **kwargs):
        student_career = get_object_or_404(StudentClassroom, pk=pk)
        student_career.is_registered = True
        student_career.is_valid = False;
        student_career.save()
        return redirect('manager_dashboard:next_level')
    
    def post(self, request, *args, **kwargs):
        semester_id = request.POST.get('semester')
        career_id = request.POST.get('career')
        
        try:
            career = ClassRoom.objects.get(pk=career_id)
            semester = Series.objects.get(pk=semester_id)
        except (ClassRoom.DoesNotExist, Series.DoesNotExist):
            raise Http404("Selected semester or career does not exist.")
        
        context = self.get_context_data(request)
        
        academic_year = AcademicYear.objects.filter(status=True, school=self.request.user.school).first()
        student_validated = StudentClassroom.objects.filter(
            semester__id=semester_id,
            career__id=career_id,
            is_valid=True, 
            is_registered=True, 
            is_next=False, 
            academic_year=academic_year
        )
        context.update({
            'career': career,
            'semester': semester,
            'student_validated':student_validated
        })
        return render(request, template_name=self.template_name, context=context)
        return super().post(request, *args, **kwargs)


class AddNextLevelView(View):
    template_name = "manager_dashboard/statistique/ajouter_monter_niveau.html"
    
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
    
    def get(self, request,pk, *args, **kwargs):
        semesters = Series.objects.filter(level__school=self.request.user.school)
        context={'semesters':semesters}
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        student_career = StudentClassroom.objects.get(pk=pk)
        student_career.is_next = True
        student_career.save()
        next_student_career = StudentClassroom.objects.create(
            student=student_career.student,
            career=student_career.career,
            academic_year=student_career.academic_year,
            semester=Series.objects.get(id=request.POST['semester']),
            is_registered=student_career.is_registered,
            school=student_career.school
        )
        next_student_career.save()
        messages.success(request, "Imformation a été modifier avec succès")
        return redirect('manager_dashboard:next_level')