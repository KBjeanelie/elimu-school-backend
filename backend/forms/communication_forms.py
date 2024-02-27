from django import forms
from ..models.communication import Information, Event
from ckeditor.widgets import CKEditorWidget

class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = '__all__'
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
        fields = '__all__'
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
