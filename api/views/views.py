from django.shortcuts import get_object_or_404
from rest_framework import generics
from api.serializers.model_serializer import AssessmentSerializer, EventSerializer, FinancialCommitmentSerializer, InformationSerializer, InvoiceSerializer, ScheduleSerializer, eBookSerializer
from backend.models.communication import Information, Event
from backend.models.contenue_pedagogique import eBook
from backend.models.evaluations import Assessment
from rest_framework.permissions import IsAuthenticated
from backend.models.facturation import FinancialCommitment, Invoice
from itertools import chain
from backend.models.gestion_ecole import AcademicYear, Schedule, StudentClassroom


class AssessmentList(generics.ListAPIView):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = user.student
        academic_year = AcademicYear.objects.get(school=user.school, status=True)
        return Assessment.objects.filter(student=student, academic_year=academic_year)

class eBookList(generics.ListAPIView):
    serializer_class = eBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return eBook.objects.filter(school=user.school)
    

class InformationList(generics.ListAPIView):
    serializer_class = InformationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Information.objects.filter(school=user.school)


class EventList(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(school=user.school)


class InvoiceList(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = user.student
        academic_year = AcademicYear.objects.get(school=user.school, status=True)
        return Invoice.objects.filter(student=student, academic_year=academic_year)

class FinancialCommitmentList(generics.ListAPIView):
    serializer_class = FinancialCommitmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = user.student
        academic_year = AcademicYear.objects.get(school=user.school, status=True)
        return FinancialCommitment.objects.filter(student=student, academic_year=academic_year)


class SchedulesList(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = user.student
        academic_year = AcademicYear.objects.get(school=user.school, status=True)
        student_career = get_object_or_404(StudentClassroom, student=student, academic_year=academic_year, is_valid=False)
        
        # Filtrer les horaires pour chaque jour de la semaine
        monday_schedule = Schedule.objects.filter(career=student_career.career, day='lundi')
        tuesday_schedule = Schedule.objects.filter(career=student_career.career, day='mardi')
        wednesday_schedule = Schedule.objects.filter(career=student_career.career, day='mercredi')
        thursday_schedule = Schedule.objects.filter(career=student_career.career, day='jeudi')
        friday_schedule = Schedule.objects.filter(career=student_career.career, day='vendredi')
        saturday_schedule = Schedule.objects.filter(career=student_career.career, day='samedi')
        
        # Combiner les résultats de toutes les requêtes
        schedules = chain(monday_schedule, tuesday_schedule, wednesday_schedule, thursday_schedule, friday_schedule, saturday_schedule)
        
        # Trier les résultats
        sorted_schedules = sorted(schedules, key=lambda schedule: schedule.start_hours)
        
        return sorted_schedules



# class StudentSchoolCareer(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         results = []
#         student = request.user.student
#         academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
#         students_career = StudentClassroom.objects.filter(student=student, school=request.user.school)
#         student_career = get_object_or_404(StudentClassroom, student=student, academic_year=academic_year, is_valid=False)
        
#         for s in students_career:
#             R = calculate_results(semester_id=s.semester.id, career_id=s.career.id, user=request.user)
#             for r in R:
#                 if r['nui'] == student_career.student.registration_number:
#                     results.append(r)

#         return Response(results)