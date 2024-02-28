from django import forms
from backend.models.contenue_pedagogique import eBook
from backend.models.gestion_ecole import Level, Teacher

# class FolderForm(forms.ModelForm):
#     class Meta:
#         model = Folder
#         fields = ['label', 'owner']
#         widgets = {
#             'label': forms.TextInput(
#                 attrs={
#                     'type': 'text',
#                     'id': 'label',
#                     'class': 'form-control',
#                     'name': 'label',
#                     'placeholder': 'nom du dossier',
#                     'required': True

#                 }
#             ),
#             'owner': forms.Select(
#                 attrs={
#                     "class": "form-control",
#                     "required": True
#                 }
#             ),
#         }

# class FileForm(forms.ModelForm):
#     class Meta:
#         model = File
#         fields = ['label', 'inFolder', 'attachement']
#         widgets = {
#             'label': forms.TextInput(
#                 attrs={
#                     'type': 'text',
#                     'id': 'label',
#                     'class': 'form-control',
#                     'name': 'label',
#                     'placeholder': 'nom du dossier',
#                     'required': True

#                 }
#             ),
#             'inFolder': forms.HiddenInput(
#                 attrs={
#                     'type':'hidden',
#                     "class": "form-control",
#                     "required": True
#                 }
#             ),
#             'attachement': forms.FileInput(
#                 attrs={
#                     "class": "form-control",
#                     "required": True
#                 }
#             ),
#         }

# class BookCategoryForm(forms.ModelForm):
#     class Meta:
#         model = BookCategory
#         fields = ['label']

# class BookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ['label', 'author', 'code_isbn', 'location', 'attachement', 'sector']

class eBookForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(eBookForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        self.fields['author'].queryset = Teacher.objects.filter(school=user.school)
        self.fields['level'].queryset = Level.objects.filter(school=user.school)

    class Meta:
        model = eBook
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'type': 'text',
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'placeholder': 'nom du dossier',
                    'required': True

                }
            ),
            'author': forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True
                }
            ),
            'level': forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True
                }
            ),
            'photo_cover': forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            'attachement': forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
