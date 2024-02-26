from django.contrib import admin
from backend.models.communication import *
from backend.models.evaluations import *
from backend.models.contenue_pedagogique import *
from backend.models.gestion_ecole import *
from backend.models.facturation import *
from backend.models import *

# Register your models here.
admin.site.register(TypeOfEvaluation)
admin.site.register(Assessment)
admin.site.register(ReportCard)

admin.site.register(Information)
admin.site.register(Event)
admin.site.register(EventParticipate)
admin.site.register(Group)
admin.site.register(DiscussionGroup)
admin.site.register(GroupMessage)
admin.site.register(GroupMedia)
admin.site.register(Contact)
admin.site.register(StudentDiscussion)
admin.site.register(StudentDiscussionMedia)

admin.site.register(Item)
admin.site.register(Invoice)
admin.site.register(FinancialCommitment)


admin.site.register(Etablishment)
admin.site.register(AcademicYear)
admin.site.register(Level)
admin.site.register(DocumentType)
admin.site.register(Program)
admin.site.register(GroupSubject)
admin.site.register(Sector)
admin.site.register(SanctionAppreciationType)
admin.site.register(Subject)
admin.site.register(Career)
admin.site.register(Semester)
admin.site.register(StudentCareer)
admin.site.register(Schedule)
admin.site.register(SanctionAppreciation)
admin.site.register(StudentDocument)
admin.site.register(TeacherDocument)

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(ManagementProfil)