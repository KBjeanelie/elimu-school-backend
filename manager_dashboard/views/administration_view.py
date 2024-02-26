from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.forms.evaluation_forms import TypeOfEvaluationForm
from backend.forms.gestion_ecole_forms import DocumentTypeForm, EtablishmentForm, SanctionAppreciationTypeForm
from backend.models.evaluations import TypeOfEvaluation
from backend.models.gestion_ecole import DocumentType, SanctionAppreciationType
from backend.forms.gestion_ecole_forms import ManagementProfilForm

class TypeEvaluationView(View):
    template_name = "manager_dashboard/administration/type_evaluations.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        type_evaluations = TypeOfEvaluation.objects.filter(school=request.user.school)
        form = TypeOfEvaluationForm()
        context = {'type_evaluations':type_evaluations, 'form':form}
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['school'] = request.user.school
        form = TypeOfEvaluationForm(data)
        if form.is_valid():
            form.save()  # Sauvegarde du nouvel objet
            return redirect('manager_dashboard:type_evaluation')
        
        type_evaluations = TypeOfEvaluation.objects.filter(school=request.user.school)
        context = {'type_evaluations':type_evaluations, 'form':form}
        return render(request, template_name=self.template_name, context=context)

class TypeEvaluationDeleteView(View):
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(TypeOfEvaluation, pk=pk)
        instance.delete()
        return JsonResponse({'message': 'Élément supprimé avec succès'})

class TypeDocumentView(View):
    template_name = "manager_dashboard/administration/type_documents.html"

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        form = DocumentTypeForm()  # Formulaire pour la création
        typeDocuments = DocumentType.objects.filter(school=request.user.school).order_by('-created_at')
        context= {'type_documents': typeDocuments, 'form':form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['school'] = request.user.school
        form = DocumentTypeForm(data)
        if form.is_valid():
            form.save()  # Sauvegarde du nouvel objet
            return redirect('manager_dashboard:type_documents')
        
        typeDocuments = DocumentType.objects.filter(school=request.user.school).order_by('-created_at')
        context = {'type_documents': typeDocuments, 'form': form}
        return render(request, template_name=self.template_name, context=context)

class TypeDocumentDeleteView(View):
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(DocumentType, pk=pk)
        instance.delete()
        return JsonResponse({'message': 'Élément supprimé avec succès'})

def get_last_document_type(request):
    last_object = DocumentType.objects.filter(school=request.user.school).last()
    document_type = {
        'id': last_object.id,
        'title': last_object.title
    }
    return JsonResponse(document_type)



class TypeSanctionView(View):
    template_name = "manager_dashboard/administration/type_sanctions.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        typeSanctions = SanctionAppreciationType.objects.filter(school=request.user.school).order_by('-created_at')
        form = SanctionAppreciationTypeForm()  # Formulaire pour la création
        context = {'type_sanctions': typeSanctions, 'form': form}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['school'] = request.user.school
        form = SanctionAppreciationTypeForm(data)  # Formulaire pour la création
        if form.is_valid():
            form.save()  # Sauvegarde du nouvel objet
            return redirect('manager_dashboard:type_sanctions')
        
        typeSanctions = SanctionAppreciationType.objects.filter(school=request.user.school).order_by('-created_at')
        context = {'type_sanctions': typeSanctions, 'form': form}
        return render(request, template_name=self.template_name, context=context)


class TypeSanctionDeleteView(View):
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(SanctionAppreciationType, pk=pk)
        instance.delete()
        return JsonResponse({'message': 'Élément supprimé avec succès'})


def get_last_sanction_type(request):
    last_object = SanctionAppreciationType.objects.filter(school=request.user.school).last()
    sanction_type = {
        'id': last_object.id,
        'title': last_object.title,
        'description': last_object.description
    }
    
    return JsonResponse(sanction_type)


class SettingAppView(View):
    template_name = "manager_dashboard/administration/reglage_generale.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        context = {'form':EtablishmentForm(instance=request.user.school)}
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = EtablishmentForm(request.POST, instance=request.user.school)
        if form.is_valid():
            form.save()
            redirect('manager_dashboard:reglage_general')
        else:
            print(form.errors)
        return render(request, template_name=self.template_name, context={'form':form})

class ProfileAppView(View):
    template_name = "manager_dashboard/administration/profil.html"

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    
    def get(self, request, *args, **kwargs):
        form = ManagementProfilForm()
        context = {'form':form}
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = ManagementProfilForm()
        context = {'form':form}
        render(request, template_name=self.template_name, context=context)
    
class EditProfileView(View):
    template_name = "manager_dashboard/administration/edit_profile.html"

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    
    def get(self, request, *args, **kwargs):
        management_profil_instance = request.user.management_profil
        form = ManagementProfilForm(instance=management_profil_instance)
        context = {'form':form}
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        management_profil_instance = request.user.management_profil
        form = ManagementProfilForm(request.POST, instance=management_profil_instance)
        if form.is_valid():
            form.save()
        return redirect('manager_dashboard:user_profile')