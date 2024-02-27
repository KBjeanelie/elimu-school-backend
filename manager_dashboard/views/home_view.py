from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Sum
from backend.models.facturation import FinancialCommitment
from backend.models.gestion_ecole import AcademicYear, StudentClassroom, Teacher
from backend.models.user_account import User

class NotAcademicYearFound(View):
    template_name = "manager_dashboard/administration/no_academique.html"
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class ManagerIndexView(View):
    template_name = "manager_dashboard/index.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        academic_year = AcademicYear.objects.filter(status=True, school=self.request.user.school).first()
        total_student = StudentClassroom.objects.filter(academic_year=academic_year, is_next=False).count()
        # Récupérer tous les engagements financiers
        if academic_year is None:
            total_engagements = 0
        else:
            engagements = FinancialCommitment.objects.filter(academic_year=academic_year)
            total_engagements = engagements.aggregate(total=Sum('school_fees'))['total'] or 0
        
        count_user = User.objects.filter(school=request.user.school).count()
        
        count_teacher = Teacher.objects.filter(school=request.user.school).count()
        context = {
            'total_student':total_student,
            'total_engagements':total_engagements,
            'count_user':count_user,
            'count_teacher':count_teacher
        }
        
        return render(request, template_name=self.template_name, context=context)