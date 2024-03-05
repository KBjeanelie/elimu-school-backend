import os
from django.db import models
from backend.models.gestion_ecole import AcademicYear, ClassRoom, Etablishment, Series, Subject
from backend.models.user_account import Student
from elimu_school import settings
from elimu_school.constant import periode_of_exam, types_evaluations, types_of_classroom


class TypeOfEvaluation(models.Model):
    title = models.CharField(max_length=50)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Sector: {self.title}"


class Assessment(models.Model):
    note = models.IntegerField(default=0)
    is_publish = models.BooleanField(default=False)
    type_evaluation = models.CharField(choices=types_evaluations, max_length=20, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True)
    period = models.CharField(choices=periode_of_exam, max_length=20, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Evaluation {self.subject} de {self.student}, note {self.note}"


class ReportCard(models.Model):
    average = models.FloatField(default=10)
    file = models.FileField(upload_to='releves_notes')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(choices=types_of_classroom, max_length=11, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"bulletin de {self.student} en {self.career}"
    
    def file_exists(self):
        if self.file:
            return os.path.exists(settings.MEDIA_ROOT / str(self.file))
        return False

    def delete(self, *args, **kwargs):
        # Supprimer le fichier associé s'il existe
        if self.file and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.file))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.file)))
        
        # Supprimer l'objet
        super(ReportCard, self).delete(*args, **kwargs)