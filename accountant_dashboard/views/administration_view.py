from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from backend.forms.facturation_forms import ItemForm
from backend.forms.gestion_ecole_forms import ManagementProfilForm
from backend.models.facturation import Item

#=============================== PARTIE CONCERNANT LES ARTICLES ==========================
class EditItemView(View):
    template = "accountant_dashboard/administration/edit_article.html"
    def get(self, request, pk, *args, **kwargs):
        item = get_object_or_404(Item, pk=pk)
        form = ItemForm(instance=item)
        context = {'form':form, 'item':item}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(Item, pk=pk)
        data = request.POST.copy()
        data['school'] = request.user.school
        form = ItemForm(data, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Article modifier avec succès !")
            return redirect('accountant_dashboard:items')
        
        messages.error(request, "ERREUR: Impossible de modifier l'article")
        context = {'form': form, 'item': item}
        return render(request, template_name=self.template, context=context)
    
class AddItemView(View):
    template = "accountant_dashboard/administration/ajout_article.html"
    def get(self, request, *args, **kwargs):
        form = ItemForm()
        context = {'form':form}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['school'] = request.user.school
        form = ItemForm(data)
        if form.is_valid():
            form.save()
            messages.success(request, "Article enregistré avec succès !")
            return redirect('accountant_dashboard:items')
        
        messages.error(request, "ERREUR: Impossible d'ajouter un article")
        context = {'form': form}
        return render(request, template_name=self.template, context=context)

class ItemView(View):
    template = "accountant_dashboard/administration/articles.html"

    def get(self, request, *args, **kwargs):
        items = Item.objects.filter(school=request.user.school).order_by('-created_at')
        context = {'items': items}
        return render(request, template_name=self.template, context=context)
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Item, pk=pk)
        instance.delete()
        items = Item.objects.filter(school=request.user.school).order_by('-created_at')
        context = {'items': items}
        return render(request, template_name=self.template, context=context)
    
#===END



class ProfileAppView(View):
    template_name = "accountant_dashboard/administration/profil.html"

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_accountant or request.user.is_admin:
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
    template_name = "accountant_dashboard/administration/edit_profile.html"

    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_accountant or request.user.is_admin:
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
            messages.success(request, "Votre profil a été modifier avec succès !")
        return redirect('accountant_dashboard:user_profile')