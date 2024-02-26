from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.forms.contenue_pedagogique_forms import eBookForm
from django.contrib import messages
from backend.models.contenue_pedagogique import  eBook

class AddeBook(View):
    template = "manager_dashboard/contenue_pedagogique/ajout_ebook.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        form = eBookForm(request.user)
        context_object = {'form': form}
        return render(request, template_name=self.template, context=context_object)
    
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['school'] = request.user.school
        form = eBookForm(request.user, data, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Le eBook {form.cleaned_data['title']} a été enregistré avec succèss !")
            return redirect('manager_dashboard:ebooks')
        
        messages.error(request, "ERREUR: Impossible d'ajouter un ebook")
        context_object = {'form': form}
        return render(request, template_name=self.template, context=context_object)

class EditEbook(View):
    template = "manager_dashboard/contenue_pedagogique/editer_ebook.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, pk, *args, **kwargs):
        ebook = get_object_or_404(eBook, pk=pk)
        form = eBookForm(request.user, instance=ebook)
        context = {'form':form, 'ebook':ebook}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        ebook = get_object_or_404(eBook, pk=pk)
        
        mutable_data = request.POST.copy()
        mutable_files = request.FILES.copy()
    
        if 'photo_cover' not in mutable_files or not mutable_files['photo_cover']:
            mutable_files['photo_cover'] = None
        if 'attachement' not in mutable_files or not mutable_files['attachement']:
            mutable_files['attachement'] = None

        mutable_data['school'] = request.user.school
        form = eBookForm(request.user, mutable_data, mutable_files, instance=ebook)
        
        if form.is_valid():
            form.save()
            messages.success(request, "eBook modifier avec succèss !")
            return redirect('manager_dashboard:ebooks')
        
        messages.error(request, "ERREUR: Impossible de modifier un ebook")
        context = {'form':form, 'ebook':ebook}
        return render(request, template_name=self.template, context=context)

class eBookView(View):
    template = 'manager_dashboard/contenue_pedagogique/ebooks.html'
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        ebooks = eBook.objects.filter(school=request.user.school)
        
        context_object = {'ebooks': ebooks}
        return render(request, template_name=self.template, context=context_object)
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(eBook, pk=pk)
        instance.delete()
        return JsonResponse({'message': 'Élément supprimé avec succès'})


# class FolderViews(View):
#     template = 'manager_dashboard/contenue_pedagogique/dossiers.html'
#     folders = Folder.objects.all().order_by('-created_at')
#     form = FolderForm()
#     contexte_object = {'folders':folders, 'form':form}
    
#     def get(self, request, *args, **kwargs):
#         return render(request, template_name=self.template, context=self.contexte_object)
    
#     def post(self, request, *args, **kwargs):
#         form = FolderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('manager_dashboard:folders')
        
#         return render(request, template_name=self.template, context=self.contexte_object)


# class FilesView(View):
#     template = 'manager_dashboard/contenue_pedagogique/fichiers.html'
    
#     def get(self, request, folder_id):
#         folder = get_object_or_404(Folder, pk=folder_id)
#         files = File.objects.filter(inFolder=folder)
#         initial_data = {'inFolder': folder}
#         form = FileForm(initial=initial_data)
#         context_object = {'files': files, 'folder': folder, 'form':form}
#         return render(request, template_name=self.template, context=context_object)
    
#     def post(self, request, *args, **kwargs):
#         form = FileForm(request.POST, request.FILES)
#         print(request.FILES)
#         print(request.POST)
#         print(form.is_valid())
#         if form.is_valid():
#             form.save()
#             redirect('manager_dashboard:content_folder')
        
#         return HttpResponse('Succès')
        
