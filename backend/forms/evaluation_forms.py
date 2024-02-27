from django import forms
from backend.models.gestion_ecole import AcademicYear, ClassRoom, Series, StudentClassroom, Subject
from backend.models.user_account import Student
from ..models.evaluations import TypeOfEvaluation, Assessment, ReportCard

class TypeOfEvaluationForm(forms.ModelForm):
    class Meta:
        model = TypeOfEvaluation
        fields = ['title', 'school']
        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'id': 'title',
                    'class': 'form-control',
                    'name': 'title',
                    'placeholder': 'cv',
                    'required': True
                }
            )
        }

class AssessmentForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(AssessmentForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        # self.fields['serie'].queryset = Series.objects.filter(level__school=user.school)
        self.fields['academic_year'].queryset = AcademicYear.objects.filter(school=user.school)
        # self.fields['classroom'].queryset = ClassRoom.objects.filter(sector__school=user.school)
        # self.fields['subject'].queryset = Subject.objects.filter(level__school=user.school)
        self.fields['type_evaluation'].queryset = TypeOfEvaluation.objects.filter(school=user.school)
        student_ids = StudentClassroom.objects.filter(academic_year__school=user.school, academic_year__status=True).values_list('student', flat=True).distinct()
        self.fields['student'].queryset = Student.objects.filter(id__in=student_ids)
        
    class Meta:
        model = Assessment
        fields = '__all__'
        widgets = {
            'note': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'is_publish':forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'type_evaluation':forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'student':forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'subject':forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'classroom':forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'academic_year':forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

class ReportCardForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ReportCardForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        # self.fields['semester'].queryset = Series.objects.filter(level__school=user.school)
        # self.fields['career'].queryset = ClassRoom.objects.filter(sector__school=user.school)
        student_ids = StudentClassroom.objects.filter(academic_year__school=user.school, academic_year__status=True).values_list('student', flat=True).distinct()
        self.fields['student'].queryset = Student.objects.filter(id__in=student_ids)
        
    class Meta:
        model = ReportCard
        fields = '__all__'
