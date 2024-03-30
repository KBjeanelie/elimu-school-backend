from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.forms.communication_forms import EventForm, InformationForm
from backend.models.communication import Event, Information
from django.contrib import messages

class EditInformationView(View):
    template = "manager_dashboard/communication/editer_information.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('manager_dashboard:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('manager_dashboard:logout')
    
    def get(self, request, pk, *args, **kwargs):
        info = get_object_or_404(Information, pk=pk)
        form = InformationForm(instance=info)
        context = {'form':form, 'info':info}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        info = get_object_or_404(Information, pk=pk)
        
        mutable_data = request.POST.copy()
        mutable_files = request.FILES.copy()
    
        if 'file' not in mutable_files or not mutable_files['file']:
            mutable_files['file'] = None
            
        mutable_data['school'] = request.user.school
        form = InformationForm(mutable_data, mutable_files, instance=info)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Information a été modifier avec succès")
            return redirect('manager_dashboard:informations')
        
        messages.error(request, "ERREUR: Impossible de modifier l'information")
        context = {'form': form, 'info': info}
        return render(request, template_name=self.template, context=context)

class AddInformationView(View):
    template = "manager_dashboard/communication/ajouter_information.html"
    form = InformationForm()
    context = {'form':form}
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('manager_dashboard:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('manager_dashboard:logout')
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template, context=self.context)
    
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['school'] = request.user.school
        form = InformationForm(data, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Information a été enregistré avec succès")
            return redirect('manager_dashboard:informations')
        
        messages.error(request, "ERREUR: Impossible d'ajouter l'information")
        context = {'informations': Information.objects.filter(school=request.user.school).order_by('-created_at')}
        return render(request, template_name=self.template, context=context)


class InformationView(View):
    template = "manager_dashboard/communication/informations.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('manager_dashboard:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('manager_dashboard:logout')
    
    def get(self, request, *args, **kwargs):
        context = {'informations': Information.objects.filter(school=request.user.school).order_by('-created_at')}
        return render(request, template_name=self.template, context=context)
    

    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Information,pk=pk)
        instance.delete()
        context = {'informations': Information.objects.filter(school=request.user.school).order_by('-created_at')}
        return render(request, template_name=self.template, context=context)


class InformationDetail(View):
    template = "manager_dashboard/communication/information_detail.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('manager_dashboard:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('manager_dashboard:logout')
    
    def get(self, request, pk, *args, **kwargs):
        info = get_object_or_404(Information, pk=pk)
        object = {'info':info}
        return render(request, template_name=self.template, context=object)



class AddEventView(View):
    template = "manager_dashboard/communication/ajouter_evenement.html"
    form = EventForm()
    context = {'form':form}
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('manager_dashboard:login')
        
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('manager_dashboard:logout')
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template, context=self.context)
    
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['school'] = request.user.school
        form = EventForm(data, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Évenement a été enregistré avec succès")
            return redirect('manager_dashboard:events')
        
        messages.error(request, "ERREUR: Impossible d'ajouter l'evenement")
        context = {'events': Event.objects.filter(school=request.user.school).order_by('-created_at')}
        return render(request, template_name=self.template, context=context)

class EditEventView(View):
    template = "manager_dashboard/communication/editer_evenement.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('manager_dashboard:login')
        
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('manager_dashboard:logout')
    
    def get(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, pk=pk)
        form = EventForm(instance=event)
        context = {'form':form, 'event':event}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, pk=pk)
        old_date1 = event.start_date
        old_date2 = event.end_date
        
        mutable_data = request.POST.copy()
        mutable_files = request.FILES.copy()
    
        if 'file' not in mutable_files or not mutable_files['file']:
            mutable_files['file'] = None
        if 'photo' not in mutable_files or not mutable_files['photo']:
            mutable_files['photo'] = None

        if 'start_date' not in request.POST or not request.POST['start_date']:
            mutable_data['start_date'] = old_date1
        if 'end_date' not in request.POST or not request.POST['end_date']:
            mutable_data['end_date'] = old_date2
        
        mutable_data['school'] = request.user.school

        form = EventForm(mutable_data, mutable_files, instance=event)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Evenement a été modifier avec succès")
            return redirect('manager_dashboard:events')
        
        messages.error(request, "ERREUR: Impossible de modifier l'évemement")
        context = {'form':form, 'event':event}
        return render(request, template_name=self.template, context=context)

class EventView(View):
    template = "manager_dashboard/communication/evenements.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('manager_dashboard:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('manager_dashboard:logout')
    
    def get(self, request, *args, **kwargs):
        context = {'events': Event.objects.filter(school=request.user.school).order_by('-created_at')}
        return render(request, template_name=self.template, context=context)
    
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Event,pk=pk)
        instance.delete()
        context = {'events': Event.objects.filter(school=request.user.school).order_by('-created_at')}
        return render(request, template_name=self.template, context=context)

class EventDetail(View):
    template = "manager_dashboard/communication/evenement_detail.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('manager_dashboard:login')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('manager_dashboard:logout')
    
    def get(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, pk=pk)
        object = {'event':event}
        return render(request, template_name=self.template, context=object)


# class GroupDiscussionView(View):
#     template = "manager_dashboard/communication/group-discussions.html"
    
#     def dispatch(self,request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('manager_dashboard:login')
        
#         if request.user.is_manager or request.user.is_admin_school:
#             return super().dispatch(request, *args, **kwargs)
        
#         return redirect('manager_dashboard:logout')
    
#     def get(self, request, *args, **kwargs):
#         groups = Group.objects.filter(school=request.user.school)
#         form = GroupForm(request.user)
#         contexte_object = {'group_discussions': groups, 'form':form}
#         return render(request, template_name=self.template, context=contexte_object)
    
#     def post(self, request, *args, **kwargs):
#         data = request.POST.copy()
#         data['school'] = request.user.school
#         form = GroupForm(request.user, data)
#         if form.is_valid():
#             form.save()
#             return redirect('manager_dashboard:discussion_group')
        
#         groups = Group.objects.filter(school=request.user.school)
#         contexte_object = {'group_discussions': groups, 'form':form}
#         return render(request, template_name=self.template, context=contexte_object)
    
#     def delete(self, request, pk, *args, **kwargs):
#         instance = get_object_or_404(Group, pk=pk)
#         instance.delete()
        
#         groups = Group.objects.filter(school=request.user.school)
#         form = GroupForm(request.user)
#         contexte_object = {'group_discussions': groups, 'form':form}
#         return render(request, template_name=self.template, context=contexte_object)
