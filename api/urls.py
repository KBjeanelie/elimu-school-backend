from django.urls import path
from api.views.views import AssessmentList, FinancialCommitmentList, SchedulesList, StudentOfUser, SubjectList, eBookList, InvoiceList, InformationList, EventList


urlpatterns = [
    path('students/', StudentOfUser.as_view()),
    path('students/<int:student_id>/schedules/', SchedulesList.as_view()),
    path('students/<int:student_id>/assessments/', AssessmentList.as_view()),
    path('students/<int:student_id>/invoices/', InvoiceList.as_view()),
    path('students/<int:student_id>/financial-commitments/', FinancialCommitmentList.as_view()),
    path('students/<int:student_id>/ebooks/', eBookList.as_view()),
    path('students/<int:student_id>/subjects/', SubjectList.as_view()),
    path('informations/', InformationList.as_view()),
    path('events/', EventList.as_view()),
    #path('parcours/', StudentSchoolCareer.as_view()),
]