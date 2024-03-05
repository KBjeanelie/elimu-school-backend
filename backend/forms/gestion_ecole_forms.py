from django import forms
from backend.models.gestion_ecole import *

class EtablishmentForm(forms.ModelForm):
    class Meta:
        model = Etablishment
        fields = ['name', 'tel', 'address', 'social_address', 'email', 'bulletin_foot', 'currency', 'système', 'status_fees', 'subscription_fees', 'month', 're_registration_fees']
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'maxLength':'120',
                    'required': True
                }
            ),
            'tel' : forms.TextInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'maxLength':'120',
                    'required': True
                }
            ),
            'address' : forms.TextInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'maxLength':'120',
                    'required': True
                }
            ),
            'email' : forms.EmailInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'maxLength':'120',
                    'required': True
                }
            ),
            'social_address' : forms.TextInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'maxLength':'120',
                }
            ),
            'currency' : forms.Select(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                }
            ),
            'bulletin_foot' : forms.TextInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'maxLength':'120',
                }
            ),
            'système' : forms.Select(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                }
            ),
            'status_fees' : forms.Select(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                }
            ),
            'subscription_fees' : forms.NumberInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                }
            ),
            're_registration_fees' : forms.NumberInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                }
            ),
            'month' : forms.NumberInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                }
            ),
            
        }

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
        widgets = {
            'lastname_one': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Nom',
                    'required': True
                }
            ),
            'firstname_one': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Prenom',
                    'required': True
                }
            ),
            'address_one': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'adresse',
                    'required': True
                }
            ),
            'tel_one': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Numéro de téléphone',
                    'required': True
                }
            ),
            'email_one': forms.EmailInput(
                attrs={
                    'type':'email',
                    'class': 'form-control',
                    'placeholder': 'email',
                }
            ),
            'picture_one': forms.FileInput(
                attrs={
                    'type':'file',
                    "class": "form-control",
                }
            ),
            'lastname_seconde': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Nom',
                }
            ),
            'firstname_seconde': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Prenom',
                }
            ),
            'address_seconde': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'adresse',
                }
            ),
            'tel_seconde': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Numéro de téléphone',
                }
            ),
            'email_seconde': forms.EmailInput(
                attrs={
                    'type':'email',
                    'class': 'form-control',
                    'placeholder': 'email',
                }
            ),
            'picture_seconde': forms.FileInput(
                attrs={
                    'type':'file',
                    "class": "form-control",
                }
            ),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['lastname', 'firstname', 'status', 'blood_type', 'birthday_place', 'allergy', 'address', 'tel', 'city', 'sex', 'email', 'bithday', 'nationality', 'picture']
        widgets = {
            'lastname': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Nom',
                    'required': True
                }
            ),
            'firstname': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Prenom',
                    'required': True
                }
            ),
            'birthday_place': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Lieu de naissance',
                }
            ),
            'allergy': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'ex: noix de coco; lactose;',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'adresse',
                }
            ),
            'nationality': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Nationalité',
                }
            ),
            'tel': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Numéro de téléphone',
                    'required': True
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'type':'email',
                    'class': 'form-control',
                    'placeholder': 'email',
                }
            ),
            'city': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'blood_type': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'sex': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required':True
                }
            ),
            'bithday':forms.DateInput(
                attrs={
                    'type':'date',
                    "class": "form-control",
                }
            ),
            'picture': forms.FileInput(
                attrs={
                    'type':'file',
                    "class": "form-control",
                }
            ),
            'status':forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            )
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['lastname', 'firstname', 'address', 'tel', 'city', 'sex', 'bithday', 'nationality', 'email', 'status', 'last_diploma', 'picture', 'start_of_contrat', 'end_of_contrat', 'school']
        widgets = {
            'lastname': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Nom',
                    'required': True
                }
            ),
            'firstname': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Prenom',
                    'required': True
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'adresse',
                }
            ),
            'last_diploma': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nationality': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Nationalité',
                }
            ),
            'tel': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Numéro de téléphone',
                    'required': True
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'type':'email',
                    'class': 'form-control',
                    'placeholder': 'email',
                    'required': True
                }
            ),
            'city': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'sex': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'bithday':forms.DateInput(
                attrs={
                    'type':'date',
                    "class": "form-control",
                }
            ),
            'start_of_contrat':forms.DateInput(
                attrs={
                    'type':'date',
                    "class": "form-control",
                }
            ),
            'end_of_contrat':forms.DateInput(
                attrs={
                    'type':'date',
                    "class": "form-control",
                }
            ),
            'picture': forms.FileInput(
                attrs={
                    'type':'file',
                    "class": "form-control",
                }
            ),
            'status':forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            )
        }

class ManagementProfilForm(forms.ModelForm):
    class Meta:
        model = ManagementProfil
        fields = ['lastname', 'firstname', 'address', 'tel', 'city', 'sex', 'email', 'bio', 'picture']
        widgets = {
            'lastname': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Nom',
                }
            ),
            'firstname': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Prenom',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'adresse',
                }
            ),
            'tel': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Numéro de téléphone',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'type':'email',
                    'class': 'form-control',
                    'placeholder': 'email',
                }
            ),
            'city': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'sex': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'picture': forms.FileInput(
                attrs={
                    'type':'file',
                    "class": "form-control",
                }
            ),
            'bio':forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows':5,
                }
            )
        }

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['label', 'start_date', 'end_date', 'status', 'school']
        widgets = {
            'label' : forms.TextInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'maxLength':'50',
                    'placeholder': 'ex: 2020 - 2021',
                    'required': True
                }
            ),
            'start_date': forms.DateInput(
                attrs={
                    'type':'date',
                    'class': 'form-control',
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'type':'date',
                    'class': 'form-control',
                }
            ),
            'status':forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            )
        }

class SeriesForm(forms.ModelForm):
    
    class Meta:
        model = Series
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'id': 'title',
                    'class': 'form-control',
                    'name': 'title',
                    'maxLength':'50',
                    'placeholder': 'ex: D',
                    'required': True
                }
            ),
        }

class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = '__all__'
        widgets = {
            'label' : forms.TextInput(
                attrs={
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'maxLength':'50',
                    'placeholder': 'ex: 1er année',
                    'required': True
                }
            ),
            'fees' : forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'cycles' : forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'serie' : forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'principal_teacher' : forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
        }

class ClassRoomForm(forms.ModelForm):

    class Meta:
        model = ClassRoom
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'type':'text',
                    'id': 'title',
                    'class': 'form-control',
                    'name': 'title',
                    'maxLength':'50',
                    'placeholder': 'Licence Informatique 1',
                    'required': True
                }
            ),
            'level': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'types': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'do_class': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
        }

class GroupSubjectForm(forms.ModelForm):
    class Meta:
        model = GroupSubject
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'type':'text',
                    'id': 'title',
                    'class': 'form-control',
                    'name': 'title',
                    'maxLength':'50',
                    'placeholder': 'ex: Matière scientifique',
                    'required': True
                }
            ),
        }

class SubjectForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        self.fields['teacher_in_charge'].queryset = Teacher.objects.filter(school=user.school)
        #self.fields['level'].queryset = Level.objects.filter(school=user.school)
        self.fields['subject_group'].queryset = GroupSubject.objects.filter(school=user.school)
        
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'label' : forms.TextInput(
                attrs={
                    'type':'text',
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'maxLength':'50',
                    'placeholder': 'Nom de la matière',
                    'required': True
                }
            ),
            'coefficient': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'teacher_in_charge': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'level': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'subject_group': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'possible_evaluation':forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'possible_averaging':forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            )
        }

class ScheduleForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        #self.fields['career'].queryset = ClassRoom.objects.filter(sector__school=user.school)
        #self.fields['subject'].queryset = Subject.objects.filter(sector__school=user.school)

    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {
            'start_hours': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'end_hours': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'day': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'subject': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'classroom': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            
        }

class ProgramForm(forms.ModelForm):
    
    class Meta:
        model = Program
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'id': 'title',
                    'class': 'form-control',
                    'name': 'title',
                    'placeholder': 'Titre du programmme',
                    'required': True
                }
            ),
            'description' : forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'description',
                    'cols':"10",
                    'rows':'5'
                }
            ),
            'level': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = ['title', 'school', 'status']
        labels = {'title': 'Titre'}
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'id': 'title',
                    'class': 'form-control',
                    'name': 'title',
                    'placeholder': 'cv',
                    'required': True
                }
            ),
            'status':forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            )
        }

class SanctionAppreciationTypeForm(forms.ModelForm):
    class Meta:
        model = SanctionAppreciationType
        fields = ['title', 'description', 'school']

class SanctionAppreciationForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(SanctionAppreciationForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = SanctionAppreciationType.objects.filter(school=user.school)
        self.fields['subject'].queryset = Subject.objects.filter(level__school=user.school)
        self.fields['classroom'].queryset = ClassRoom.objects.filter(level__school=user.school)
        student_ids = StudentClassroom.objects.filter(academic_year__school=user.school, academic_year__status=True).values_list('student', flat=True).distinct()
        self.fields['student'].queryset = Student.objects.filter(id__in=student_ids)
        
    class Meta:
        model = SanctionAppreciation
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'description',
                    'cols':"10",
                    'rows':'5'
                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'subject': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'student': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'classroom': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
        }

class StudentDocumentForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(StudentDocumentForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        self.fields['document_type'].queryset = DocumentType.objects.filter(school=user.school)
        
    class Meta:
        model = StudentDocument
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'type':'text',
                    'id': 'title',
                    'class': 'form-control',
                    'name': 'title',
                    'maxLength':'50',
                    'placeholder': 'Titre du document',
                    'required': True
                }
            ),
            'document_type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'student': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
        }

class TeacherDocumentForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(TeacherDocumentForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        self.fields['document_type'].queryset = DocumentType.objects.filter(school=user.school)
        
    class Meta:
        model = TeacherDocument
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'type':'text',
                    'id': 'title',
                    'class': 'form-control',
                    'name': 'title',
                    'maxLength':'50',
                    'placeholder': 'Titre du document',
                    'required': True
                }
            ),
            'document_type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'teacher': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
        }