from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.db.models import Sum
from backend.models.facturation import FinancialCommitment
from backend.models.gestion_ecole import AcademicYear, Etablishment, Parent, StudentClassroom, Teacher
from django.contrib import messages
from backend.forms.user_account_forms import LoginForm
from backend.models.user_account import User

class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(to='manager_dashboard:login')

class LoginView(View):
    template_name = "manager_dashboard/login.html"
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)
    
    def post(self, request, *args, **kwargs):
        sign_form = LoginForm(request.POST)
        code = request.POST['code']
        try:
            school = Etablishment.objects.get(code=code)
        except Etablishment.DoesNotExist:
            messages.error(request, "ERREUR: Aucun établissement ne corresponds à ce code")
            return redirect(to='manager_dashboard:login')
        
        username = sign_form['username'].value()
        try:
            User.objects.get(school=school, username=username)
        except User.DoesNotExist:
            messages.error(request, "ERREUR: Aucun utilisateur ne corresponds à cet établissement")
            return redirect(to='manager_dashboard:login')
        
        password = sign_form['password'].value()
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "ERREUR: Mot de passe incorrect :(")
            return redirect(to='manager_dashboard:login')
        
        login(request, user)
    
        years = AcademicYear.objects.filter(school=user.school)
        
        for academic_year in years:
            if academic_year.status:
                request.session['academic_year'] = academic_year.label
                request_student = StudentClassroom.objects.filter(academic_year=academic_year, is_registered=False).count()
                request.session['request_student'] = request_student
                break

        if user.is_manager or user.is_admin_school:
            return redirect(to='manager_dashboard:index')
        elif user.is_accountant:
            return redirect(to='accountant_dashboard:index')
        else:
            messages.error(request, "ERREUR: Vous n'avez pas droit à accéder à cette partie :(")
            return redirect(to='manager_dashboard:login')


class NotAcademicYearFound(View):
    template_name = "manager_dashboard/administration/no_academique.html"
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class ManagerIndexView(View):
    template_name = "manager_dashboard/index.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('manager_dashboard:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('manager_dashboard:logout')
    
    def get(self, request, *args, **kwargs):
        academic_year = AcademicYear.objects.filter(status=True, school=self.request.user.school).first()
        total_student = StudentClassroom.objects.filter(academic_year=academic_year, is_next=False).count()
        students = StudentClassroom.objects.filter(academic_year=academic_year, is_registered=True, is_valid=False).order_by('-created_at')[:10]

        # Récupérer tous les engagements financiers
        if academic_year is None:
            total_engagements = 0
        else:
            engagements = FinancialCommitment.objects.filter(academic_year=academic_year)
            total_engagements = engagements.aggregate(total=Sum('school_fees'))['total'] or 0
        
        count_parent = Parent.objects.filter(school=request.user.school).count()
        
        count_teacher = Teacher.objects.filter(school=request.user.school).count()
        context = {
            'total_student':total_student,
            'total_engagements':total_engagements,
            'count_parent':count_parent,
            'count_teacher':count_teacher,
            'student_careers':students
        }
        
        return render(request, template_name=self.template_name, context=context)