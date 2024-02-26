from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.forms.gestion_ecole_forms import EtablishmentForm
from backend.models.gestion_ecole import Etablishment, Student, Teacher
from backend.models.user_account import User
from django.contrib import messages

# Create your views here.
class IndexView(View):
    template_name = "administration/index.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return redirect('backend:login')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        count_school = Etablishment.objects.all().count()
        count_user = User.objects.all().count()
        count_teacher = Teacher.objects.all().count()
        count_student = Student.objects.filter(is_valid=True, status=True).count()
        context = {
            'count_user':count_user,
            'count_teacher':count_teacher,
            'count_student':count_student,
            'count_school':count_school
        }
        return render(request, template_name=self.template_name, context=context)


class SchoolsView(View):
    template_name = "administration/schools/schools.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return redirect('backend:login')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        schools = Etablishment.objects.all()
        return render(request, template_name=self.template_name, context={'schools':schools})
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Etablishment, pk=pk)
        instance.delete()
        return JsonResponse({'message': 'Élément supprimé avec succès'})


class AddSchoolView(View):
    template_name = "administration/schools/ajout_school.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return redirect('backend:login')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = EtablishmentForm()
        return render(request, template_name=self.template_name, context={'form':form})
    
    def post(self, request, *args, **kwargs):
        form = EtablishmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'établissement a été enregistré avec succès !")
            return redirect('administration:schools')
        
        messages.error(request, "ERREUR: Impossible d'enregistré l'établissement")
        return render(request, template_name=self.template_name, context={'form':form})

class UserSchoolView(View):
    template_name = "administration/users/user_school.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return redirect('backend:login')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_admin_school=True)
        return render(request, template_name=self.template_name, context={'users':users})
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Etablishment, pk=pk)
        instance.delete()
        return JsonResponse({'message': 'Élément supprimé avec succès'})


class AddUserSchoolView(View):
    template_name = "administration/users/add_user.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return redirect('backend:login')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        schools = Etablishment.objects.all()
        return render(request, template_name=self.template_name, context={'schools':schools})
    
    def post(self, request, *args, **kwargs):
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user:
            user.is_admin_school = True
            user.school = Etablishment.objects.get(id=request.POST['school'])
            user.save()
            messages.success(request, "Utilisateur admin enregistré avec succès !")
            return redirect('administration:user_school')
        
        messages.error(request, "ERREUR: Impossible d'enregistré l'utilisateur :(")
        schools = Etablishment.objects.all()
        return render(request, template_name=self.template_name, context={'schools':schools})