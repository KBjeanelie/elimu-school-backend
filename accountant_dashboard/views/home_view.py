from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.models.facturation import FinancialCommitment
from django.db.models import Sum
from backend.models.gestion_ecole import AcademicYear, StudentClassroom, Teacher
from backend.models.user_account import Student, User
from django.contrib import messages


class AccountantIndexView(View):
    template_name = "accountant_dashboard/index.html"
    
    def get(self, request, *args, **kwargs):
        count_user = User.objects.filter(school=request.user.school).count()

        try:
            academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
            # Récupérer tous les engagements financiers
            engagements = FinancialCommitment.objects.filter(academic_year=academic_year)
            total_engagements = engagements.aggregate(total=Sum('school_fees'))['total'] or 0
        except AcademicYear.DoesNotExist:
            total_engagements = 0
            academic_year = False
        
        total_student = StudentClassroom.objects.filter(academic_year=academic_year, is_next=False).count()
        count_teacher = Teacher.objects.filter(school=request.user.school).count()
        context = {
            'count_user':count_user,
            'total_engagements':total_engagements,
            'academic_year':academic_year,
            'total_student':total_student,
            'count_teacher':count_teacher
        }
        return render(request, template_name=self.template_name, context=context)

class NotAcademicYearFound(View):
    template_name = "accountant_dashboard/administration/no_academique.html"
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

#================================
class PreRegistrationView(View):
    template = "accountant_dashboard/communication/pre-inscription.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            academic_year = AcademicYear.objects.get(status=True, school=request.user.school)
            students = StudentClassroom.objects.filter(academic_year=academic_year, is_registered=False).order_by('-created_at')
            context = {'student_careers':students, 'year':academic_year}
            return render(request, template_name=self.template, context=context)
        except AcademicYear.DoesNotExist:
            # Exécuter du code alternatif si l'objet AcademicYear n'existe pas
           return render(request, template_name=self.template)
        

class PreRegistrationDetailView(View):
    template = "accountant_dashboard/communication/pre-inscription_detail.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        academic_year = AcademicYear.objects.get(status=True, school=request.user.school)
        student_career = get_object_or_404(StudentClassroom, pk=pk, academic_year=academic_year)
        context = {'student_career':student_career}
        return render(request, template_name=self.template, context=context)
    
    def check(self, pk, *args, **kwargs):
        student_career = get_object_or_404(StudentClassroom, pk=pk)
        student_career.is_registered = True
        student_career.save()
        
        if student_career.student:
            student_career.student.is_valid = True
            student_career.student.status = True
            student_career.student.save()
            
            #enregistrer un engagement financiers
            amount_level = student_career.classroom.level.fees * 9
            financialCommitment = FinancialCommitment.objects.create(
                student=student_career.student,
                academic_year=student_career.academic_year,
                school_fees=amount_level
            )
            financialCommitment.save()
        return redirect('accountant_dashboard:pre_registrations')
    
    def delete(self, pk, *args, **kwargs):
        student_career = get_object_or_404(StudentClassroom, pk=pk)
        student = get_object_or_404(Student, id=student_career.student.id)
        student_career.delete()
        student.delete()
        return redirect('accountant_dashboard:pre_registrations')
#===END