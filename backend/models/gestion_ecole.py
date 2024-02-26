import os
from django.db import models
from elimu_school import settings
from elimu_school.constant import days_of_the_weeks, hours_of_the_day, currencies, systemes, statues
import uuid

class Etablishment(models.Model):
    name = models.CharField(max_length=120)
    tel = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    social_address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    bulletin_foot = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=50, choices=currencies, blank=True, null=True)
    système = models.CharField(max_length=50, choices=systemes, blank=True, null=True)
    status_fees = models.CharField(max_length=50, choices=statues, blank=True, null=True)
    subscription_fees = models.IntegerField(default=1000, blank=True, null=True)
    month = models.IntegerField(default=9, blank=True, null=True)
    re_registration_fees = models.IntegerField(default=800, blank=True, null=True)
    
    def __str__(self):
        return f"Etablissement: {self.name}"


last_diploma = (
    ('Doctorat', 'Doctorat'),
    ('Master', 'Master'),
    ('Licence', 'Licence'),
    ('DUT', 'DUT'),
    ('Baccalauréat', 'Baccalauréat')
)
cities = (
    ('pointe_noire', "Pointe Noire"),
    ('brazzaville', "Brazzaville")
)

type_blood = (
    ('O+', "O+"),
    ('O-', "O-"),
    ('A+', "A+"),
    ('A-', "A-"),
    ('B+', "B+"),
    ('B-', "B-"),
    ('AB+', "AB+"),
    ('AB-', "AB-"),
)

sexes = (
    ('masculin', 'Masculin'),
    ('feminin', 'Féminin')
)

#=============================================================================================================================
#=================================== CE SONT LES MODEL REPRÉSENTANT CHAQUE PROFIL UTILISATEUR DE L'APP =======================
# Represent an objet of Student and his profil info

import hashlib

class ShortUUID4Field(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 15)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('editable', False)
        super().__init__(*args, **kwargs)

    def generate_short_uuid(self):
        full_uuid = uuid.uuid4().hex
        short_uuid = hashlib.sha1(full_uuid.encode('utf-8')).hexdigest()[:15]
        return short_uuid

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value:
            value = self.generate_short_uuid()
            setattr(model_instance, self.attname, value)
        return value
        
class Student(models.Model):
    
    registration_number = ShortUUID4Field()
    
    lastname = models.CharField(max_length=50, null=True, blank=True)
    
    firstname = models.CharField(max_length=50, null=True, blank=True)
    
    address = models.CharField(max_length=50, null=True, blank=True)
    
    tel = models.CharField(max_length=20, blank=True)
    
    city = models.CharField(max_length=17, choices=cities, blank=True)
    
    sex = models.CharField(max_length=10, choices=sexes, blank=True)
    
    email = models.CharField(max_length=120, unique=True, blank=True, null=True)
    
    bithday = models.DateField(null=True, blank=True)
    
    nationality = models.CharField(max_length=20, blank=True)
    
    blood_type = models.CharField(max_length=5, blank=True, null=True, choices=type_blood)
    
    birthday_place = models.CharField(max_length=100, blank=True, null=True)
    
    allergy = models.CharField(max_length=255, blank=True, null=True)
    
    picture = models.ImageField(upload_to="student_images", blank=True, null=True)
    
    status = models.BooleanField(default=False)
    
    is_valid = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.registration_number} - {self.lastname} {self.firstname}"
    
    def fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    def file_exists(self):
        if self.picture:
            return os.path.exists(settings.MEDIA_ROOT / str(self.picture))
        return False
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier associé s'il existe
        if self.picture and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.picture))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.picture)))
        
        # Supprimer l'objet
        super(Student, self).delete(*args, **kwargs)


# Represent an objet of Teacher and his profil info
class Teacher(models.Model):
    
    lastname = models.CharField(max_length=50, blank=True)
    
    firstname = models.CharField(max_length=50, blank=True)
    
    address = models.CharField(max_length=50, blank=True)
    
    tel = models.CharField(max_length=20, blank=True)
    
    city = models.CharField(max_length=17, choices=cities, blank=True)
    
    sex = models.CharField(max_length=10, choices=sexes, blank=True)
    
    bithday = models.DateField(blank=True, null=True)
    
    nationality = models.CharField(max_length=20, blank=True)
    
    email = models.CharField(max_length=120, unique=True, blank=True)
    
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True, blank=True)
    
    status = models.CharField(max_length=20, blank=True)
    
    last_diploma = models.CharField(max_length=20, choices=last_diploma, blank=True,)
    
    picture = models.ImageField(upload_to="teacher_images", blank=True, null=True)
    
    type_of_counter = models.CharField(max_length=20, blank=True)
    
    start_of_contrat = models.DateField(blank=True, null=True)
    
    end_of_contrat = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"Enseignant : {self.lastname} - {self.firstname}"
    
    def fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    def file_exists(self):
        if self.picture:
            return os.path.exists(settings.MEDIA_ROOT / str(self.picture))
        return False
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier associé s'il existe
        if self.picture and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.picture))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.picture)))
        
        # Supprimer l'objet
        super(Teacher, self).delete(*args, **kwargs)



# Represent an objet of team manager and his profil info
class ManagementProfil(models.Model):

    lastname = models.CharField(max_length=50, blank=True)
    
    firstname = models.CharField(max_length=50, blank=True)
    
    address = models.CharField(max_length=50, blank=True)
    
    tel = models.CharField(max_length=20, blank=True)
    
    city = models.CharField(max_length=17, choices=cities, blank=True)
    
    sex = models.CharField(max_length=10, choices=sexes, blank=True)
    
    email = models.CharField(max_length=120, unique=True, blank=True, null=True)
    
    picture = models.ImageField(upload_to="managements_images", blank=True, null=True)
    
    bio = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier associé s'il existe
        if self.picture and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.picture))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.picture)))
        
        # Supprimer l'objet
        super(ManagementProfil, self).delete(*args, **kwargs)
#===END


# Class representing Academic Year
class AcademicYear(models.Model):
    label = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=True)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Academic Year: {self.label}"

# Class representing Academic Level
class Level(models.Model):
    label = models.CharField(max_length=50)
    fees = models.IntegerField(default=1000)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Level: {self.label}"

# Class representing Semester
class Semester(models.Model):
    title = models.CharField(max_length=50)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Semester: {self.title}"

# Class representing Academic Program
class Program(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    program_date = models.DateField(blank=True)
    person_in_charge = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.FileField(upload_to='programmes', blank=True)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Programme : {self.title} par {self.person_in_charge}"
    
    def file_exists(self):
        if self.file:
            return os.path.exists(settings.MEDIA_ROOT / str(self.file))
        return False
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier associé s'il existe
        if self.file and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.file))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.file)))
        
        # Supprimer l'objet
        super(Program, self).delete(*args, **kwargs)

# Class representing Document Type
class DocumentType(models.Model):
    title = models.CharField(max_length=50)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Document Type: {self.title}"

# Class representing Sanction Appreciation Type
class SanctionAppreciationType(models.Model):
    title = models.CharField(max_length=50)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Sanction Appreciation Type: {self.title}"

# Class representing Document
class StudentDocument(models.Model):
    title = models.CharField(max_length=50)
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.FileField(upload_to='student_documents')
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Document: {self.title}"
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier associé s'il existe
        if self.file and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.file))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.file)))
        
        # Supprimer l'objet
        super(StudentDocument, self).delete(*args, **kwargs)

class TeacherDocument(models.Model):
    title = models.CharField(max_length=50)
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='teacher_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Document: {self.title}"
    
    def delete(self, *args, **kwargs):
        # Supprimer le fichier associé s'il existe
        if self.file and os.path.exists(os.path.join(settings.MEDIA_ROOT, str(self.file))):
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.file)))
        
        # Supprimer l'objet
        super(TeacherDocument, self).delete(*args, **kwargs)

# Class representing Group Subject
class GroupSubject(models.Model):
    title = models.CharField(max_length=50)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Group Subject: {self.title}"

# Class representing Sector (Field of Study)
class Sector(models.Model):
    title = models.CharField(max_length=50)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Sector: {self.title}"

# Class representing Subject
class Subject(models.Model):
    label = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, blank=True, null=True)
    teacher_in_charge = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, blank=True, null=True)
    types = [('obligatory', 'Obligatory'), ('secondary', 'Secondary')]
    type = models.CharField(max_length=12, choices=types)
    subject_group = models.ForeignKey(GroupSubject, on_delete=models.SET_NULL, null=True, blank=True)
    possible_evaluation = models.BooleanField(default=True)
    possible_averaging = models.BooleanField(default=True)
    coefficient = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Matiere : {self.label}"

# Class representing Career (Educational Program/Path)
class Career(models.Model):
    title = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Career: {self.title}"

# Class representing Student Career (Association between students and careers)
class StudentCareer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, blank=True, null=True)
    is_registered =  models.BooleanField(default=False)
    is_valid =  models.BooleanField(default=False)
    is_next = models.BooleanField(default=False)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Parcours : {self.student} en {self.career}"

# Class representing Schedule (Class Timetable)
class Schedule(models.Model):
    start_hours = models.CharField(max_length=15, choices=hours_of_the_day)
    end_hours = models.CharField(max_length=15, choices=hours_of_the_day)
    day = models.CharField(max_length=10, choices=days_of_the_weeks)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Class Schedule for: {self.subject}"

# Class representing Sanction Appreciation (Student Discipline)
class SanctionAppreciation(models.Model):
    comment = models.TextField(blank=True)
    type = models.ForeignKey(SanctionAppreciationType, on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, blank=True, null=True)
    sanction_date = models.DateField(blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Sanction de {self.student} pour {self.comment}"
