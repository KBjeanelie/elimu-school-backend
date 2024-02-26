from django.urls import path
from api.views.views import AssessmentList, FinancialCommitmentList, SchedulesList, StudentSchoolCareer, eBookList, InvoiceList, InformationList, EventList


urlpatterns = [
    path('schedules/', SchedulesList.as_view()),
    path('assessments/', AssessmentList.as_view()),
    path('invoices/', InvoiceList.as_view()),
    path('ebooks/', eBookList.as_view()),
    path('informations/', InformationList.as_view()),
    path('events/', EventList.as_view()),
    path('engagements/', FinancialCommitmentList.as_view()),
    path('parcours/', StudentSchoolCareer.as_view()),
]