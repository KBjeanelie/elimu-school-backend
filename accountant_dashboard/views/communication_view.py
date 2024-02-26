from django.shortcuts import redirect, render
from django.views import View

from backend.models.communication import Event, Information
from backend.models.gestion_ecole import AcademicYear


class InformationsView(View):
    template_name = "accountant_dashboard/communication/informations.html"
    
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
        object = {'informations': Information.objects.filter(status=True, school=request.user.school)}
        return render(request, template_name=self.template_name, context=object)

class EventsView(View):
    template_name = "accountant_dashboard/communication/evenements.html"
    
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
        object = {'events': Event.objects.filter(status=True, school=request.user.school)}
        return render(request, template_name=self.template_name, context=object)