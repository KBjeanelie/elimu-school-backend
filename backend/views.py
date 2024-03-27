from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from backend.forms.user_account_forms import LoginForm
from backend.models.gestion_ecole import AcademicYear, StudentClassroom


# Create your views here.
class LogoutView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_admin:
            logout(request)
            return redirect(to='administration:login')
        return redirect('backend:login')


class LoginView(View):

    def post(self, request, *args, **kwargs):
        sign_form = LoginForm(request.POST)
        username = sign_form['username'].value()
        password = sign_form['password'].value()
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "ERREUR: Utilisateur ou mot de passe incorrect :(")
            return redirect(to='backend:login')
        
        login(request, user)
        
        years = AcademicYear.objects.filter(school=user.school)
        
        
        for academic_year in years:
            if academic_year.status:
                request.session['academic_year'] = academic_year.label
                break

        if user.is_manager or user.is_admin_school:
            return redirect(to='manager_dashboard:index')
        elif user.is_accountant:
            return redirect(to='accountant_dashboard:index')
        elif user.is_admin:
            return redirect(to='administration:index')
        else:
            messages.error(request, "ERREUR: Vous n'avez pas droit à accéder à cette partie :(")
            return redirect(to='backend:login')