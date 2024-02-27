from django import forms

from backend.models.gestion_ecole import AcademicYear, ClassRoom, StudentClassroom
from backend.models.user_account import Student
from ..models.facturation import Invoice, Item, Repayment, Spend

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'default_amount', 'defaut_quantity', 'is_active', 'analytic_code', 'school']
        
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'type': 'text',
                    'id': 'label',
                    'class': 'form-control',
                    'name': 'label',
                    'placeholder': 'ex: Frais scolaire',
                    'required': True

                }
            ),
            'default_amount' : forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': True

                }
            ),
            'defaut_quantity' : forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': True

                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'analytic_code': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            )
        }

class InvoiceForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        # self.fields['career'].queryset = ClassRoom.objects.filter(sector__school=user.school)
        self.fields['item'].queryset = Item.objects.filter(school=user.school)
        student_ids = StudentClassroom.objects.filter(academic_year__school=user.school, academic_year__status=True).values_list('student', flat=True).distinct()
        self.fields['student'].queryset = Student.objects.filter(id__in=student_ids)
    
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'student': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'classroom': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'item': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'invoice_status': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols':'3',
                    'rows':'3'
                }
            )
        }


class RepaymentForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(RepaymentForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        academic_year = AcademicYear.objects.get(school=user.school, status=True)
        self.fields['invoice'].queryset = Invoice.objects.filter(academic_year=academic_year)
    
    class Meta:
        model = Repayment
        fields = ['invoice', 'amount', 'repayment_method',  'comment', 'status', 'academic_year']
        widgets = {
            'status': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'invoice': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            
            'repayment_method': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols':'3',
                    'rows':'3'
                }
            )
        }

class SpendForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(SpendForm, self).__init__(*args, **kwargs)
        # Filtrer les niveaux en fonction de l'utilisateur connecté
        self.fields['item'].queryset = Item.objects.filter(school=user.school)
    
    class Meta:
        model = Spend
        fields = ['item', 'amount', 'comment',  'academic_year']
        widgets = {
            'item': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols':'3',
                    'rows':'3'
                }
            )
        }

