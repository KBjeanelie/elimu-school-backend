from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.forms.gestion_ecole_forms import ScheduleForm
from backend.models.gestion_ecole import AcademicYear, ClassRoom, Schedule, Series
from django.contrib import messages

class AddScheduleView(View):
    template = 'manager_dashboard/gestion_temps/ajout_emplois_temps.html'
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('manager_dashboard:no_year')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        form = ScheduleForm(request.user)
        context = {'form':form}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, *args, **kwargs):
        form = ScheduleForm(request.user, request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Cours a été enregistré avec succès")
            return redirect('manager_dashboard:times')
        
        messages.error(request, "ERREUR: Impossible d'enregistré le cours")
        context = {'form':form}
        return render(request, template_name=self.template, context=context)


class ScheduleView(View):
    template = 'manager_dashboard/gestion_temps/emplois_temps.html'
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('manager_dashboard:no_year')
        
        if request.user.is_manager or request.user.is_admin_school:
            return super().dispatch(request, *args, **kwargs)
        
        return redirect('backend:logout')
    
    def get(self, request, *args, **kwargs):
        semesters = Series.objects.filter(level__school=request.user.school)
        careers = ClassRoom.objects.filter(sector__school=request.user.school)
        context = {
            'semesters':semesters,
            'careers':careers,
        }
        return render(request, template_name=self.template, context=context)
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Schedule, pk=pk)
        instance.delete()
        return JsonResponse({'message': 'Élément supprimé avec succès'})
    
    def post(self, request, *args, **kwargs):
        #semester_id = request.POST['semester']
        career_id = request.POST['career']
        career = ClassRoom.objects.get(pk=career_id)
        
        monday_schedule = Schedule.objects.filter(career__id=career_id, day='lundi').order_by('start_hours')
        tueday_schedule = Schedule.objects.filter(career__id=career_id, day='mardi').order_by('start_hours')
        wednesday_schedule = Schedule.objects.filter(career__id=career_id, day='mercredi').order_by('start_hours')
        thursday_schedule = Schedule.objects.filter(career__id=career_id, day='jeudi').order_by('start_hours')
        friday_schedule = Schedule.objects.filter(career__id=career_id, day='vendredi').order_by('start_hours')
        saturday_schedule = Schedule.objects.filter(career__id=career_id, day='samedi').order_by('start_hours')
        
        semesters = Series.objects.filter(level__school=request.user.school)
        careers = ClassRoom.objects.filter(sector__school=request.user.school)
        
        context = {
            'semesters':semesters,
            'careers':careers,
            'monday_schedule':monday_schedule,
            'tueday_schedule':tueday_schedule,
            'wednesday_schedule':wednesday_schedule,
            'thursday_schedule':thursday_schedule,
            'friday_schedule':friday_schedule,
            'saturday_schedule':saturday_schedule,
            'career':career
        }
        return render(request, template_name=self.template, context=context)
    
    