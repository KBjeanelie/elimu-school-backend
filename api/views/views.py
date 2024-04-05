from django.shortcuts import get_object_or_404
from rest_framework import generics
from api.serializers.model_serializer import AssessmentSerializer, EventSerializer, FinancialCommitmentSerializer, InformationSerializer, InvoiceSerializer, ScheduleSerializer, StudentSerializer, SubjectSerializer, eBookSerializer
from backend.models.communication import Information, Event
from backend.models.contenue_pedagogique import eBook
from backend.models.evaluations import Assessment
from rest_framework.permissions import IsAuthenticated
from backend.models.facturation import FinancialCommitment, Invoice
from itertools import chain
from backend.models.gestion_ecole import AcademicYear, Schedule, Student, StudentClassroom, Subject

class SubjectList(generics.ListAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student_id = self.kwargs.get('student_id')
        academic_year = AcademicYear.objects.get(school=user.school, status=True)
        student_classroom = StudentClassroom.objects.get(
            academic_year=academic_year,
            student__id=student_id,
            is_registered=True,
            is_archive=False)

        # Récupérer le niveau de la classe de l'étudiant
        student_level = student_classroom.classroom.level

        # Filtrer les matières en fonction du niveau de la classe de l'étudiant
        return Subject.objects.filter(level=student_level)



class AssessmentList(generics.ListAPIView):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')  # Récupérer l'ID de l'étudiant passé en paramètre
        academic_year = AcademicYear.objects.get(school=self.request.user.school, status=True)
        return Assessment.objects.filter(student__id=student_id, academic_year=academic_year)


class eBookList(generics.ListAPIView):
    serializer_class = eBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student_id = self.kwargs.get('student_id')
        academic_year = AcademicYear.objects.get(school=user.school, status=True)
        student_classroom = StudentClassroom.objects.get(
            academic_year=academic_year,
            student__id=student_id,
            is_registered=True,
            is_archive=False)

        # Récupérer le niveau de la classe de l'étudiant
        student_level = student_classroom.classroom.level

        # Filtrer les livres électroniques en fonction du niveau de la classe de l'étudiant
        return eBook.objects.filter(school=user.school, level=student_level)
    

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

class StudentOfUser(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(parent=user.parent)

class InvoiceList(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')  # Récupérer l'ID de l'étudiant passé en paramètre
        academic_year = AcademicYear.objects.get(school=self.request.user.school, status=True)
        return Invoice.objects.filter(student__id=student_id, academic_year=academic_year)

class FinancialCommitmentList(generics.ListAPIView):
    serializer_class = FinancialCommitmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')  # Récupérer l'ID de l'étudiant passé en paramètre
        academic_year = AcademicYear.objects.get(school=self.request.user.school, status=True)
        return FinancialCommitment.objects.filter(student__id=student_id, academic_year=academic_year)


class SchedulesList(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        user = self.request.user
        academic_year = AcademicYear.objects.get(school=user.school, status=True)
        student_career = get_object_or_404(StudentClassroom, student__id=student_id, academic_year=academic_year, is_valid=False)
        
        # Filtrer les horaires pour chaque jour de la semaine
        monday_schedule = Schedule.objects.filter(classroom=student_career.classroom, day='lundi')
        tuesday_schedule = Schedule.objects.filter(classroom=student_career.classroom, day='mardi')
        wednesday_schedule = Schedule.objects.filter(classroom=student_career.classroom, day='mercredi')
        thursday_schedule = Schedule.objects.filter(classroom=student_career.classroom, day='jeudi')
        friday_schedule = Schedule.objects.filter(classroom=student_career.classroom, day='vendredi')
        saturday_schedule = Schedule.objects.filter(classroom=student_career.classroom, day='samedi')
        
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