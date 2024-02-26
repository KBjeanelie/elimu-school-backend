from django import forms

from backend.models.gestion_ecole import Career
from ..models.communication import Information, Event, Group, GroupMedia
from ckeditor.widgets import CKEditorWidget

class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['title', 'date_info', 'content', 'file', 'status', 'school']
        widgets = {
            'content': CKEditorWidget(),
            'status': forms.CheckboxInput(
                attrs={
                    'class':'form-check-input'
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Titre',
                    'required': True
                }
            ),
            'date_info':forms.DateInput(
                attrs={
                    'type':'date',
                    "class": "form-control",
                }
            ),
            'file': forms.FileInput(
                attrs={
                    'type':'file',
                    "class": "form-control",
                }
            ),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_date', 'end_date', 'content', 'file', 'status', 'photo', 'school']
        widgets = {
            'content': CKEditorWidget(),
            'status': forms.CheckboxInput(
                attrs={
                    'class':'form-check-input'
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'type':'text',
                    'class': 'form-control',
                    'placeholder': 'Titre',
                    'required': True
                }
            ),
            'start_date':forms.DateInput(
                attrs={
                    'type':'date',
                    "class": "form-control",
                }
            ),
            'end_date':forms.DateInput(
                attrs={
                    'type':'date',
                    "class": "form-control",
                }
            ),
            'file': forms.FileInput(
                attrs={
                    'type':'file',
                    "class": "form-control",
                }
            ),
            'photo': forms.FileInput(
                attrs={
                    'type':'file',
                    "class": "form-control",
                }
            ),
        }


class GroupForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        self.fields['career'].queryset = Career.objects.filter(sector__school=user.school)
        
    class Meta:
        model = Group
        fields = ['title', 'career', 'school']
        
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'type': 'text',
                    'id': 'title',
                    'class': 'form-control',
                    'name': 'title',
                    'placeholder': 'nom du group',
                    'required': True

                }
            ),
            'career': forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True
                }
            ),
        }

class GroupMediaForm(forms.ModelForm):
    class Meta:
        model = GroupMedia
        fields = ['discussion_group', 'legend', 'file']
