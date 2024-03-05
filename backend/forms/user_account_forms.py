from django import forms
from backend.models.gestion_ecole import Student, StudentClassroom
from backend.models.user_account import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

        widgets = {
            'username': forms.EmailInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "InputEmail",
                    "placeholder": "Nom d'utilisateur",
                    "required": True
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    "type": "password",
                    "class": "form-control",
                    "id": "InputPassword",
                    "placeholder": "Mot de passe",
                    "required": True
                }
            )
        }



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'student', 'teacher', 'management_profil', 'is_active', 'is_admin', 'is_manager', 'is_accountant', 'is_student', 'is_teacher']

class UserTeacherForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'teacher', 'is_active', 'is_teacher', 'password']
        
        widgets = {
            'teacher': forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'type': 'text',
                    'id': 'username',
                    'class': 'form-control',
                    'name': 'username',
                    'placeholder': 'kbjeanelie',
                    'required': True

                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'type': 'password',
                    'id': 'password',
                    'class': 'form-control',
                    'name': 'password',
                    'placeholder': '************',
                    'required': True

                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            'is_teacher': forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }




class UserStudentForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UserStudentForm, self).__init__(*args, **kwargs)
        student_ids = StudentClassroom.objects.filter(academic_year__school=user.school, academic_year__status=True).values_list('student', flat=True).distinct()
        self.fields['student'].queryset = Student.objects.filter(id__in=student_ids)
    class Meta:
        model = User
        fields = ['username', 'student', 'is_active', 'is_student', 'password']
        
        widgets = {
            'student': forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'type': 'text',
                    'id': 'username',
                    'class': 'form-control',
                    'name': 'username',
                    'placeholder': 'kbjeanelie',
                    'required': True

                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'type': 'password',
                    'id': 'password',
                    'class': 'form-control',
                    'name': 'password',
                    'placeholder': '************',
                    'required': True

                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            'is_student': forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class UserParentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'parent', 'is_active', 'is_parent', 'password']
        
        widgets = {
            'parent': forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'type': 'text',
                    'id': 'username',
                    'class': 'form-control',
                    'name': 'username',
                    'placeholder': 'kbjeanelie',
                    'required': True

                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'type': 'password',
                    'id': 'password',
                    'class': 'form-control',
                    'name': 'password',
                    'placeholder': '************',
                    'required': True

                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            'is_parent': forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }
