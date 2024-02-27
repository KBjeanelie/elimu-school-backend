from django.db import models
from backend.models.gestion_ecole import AcademicYear, ClassRoom, Etablishment
from backend.models.user_account import Student
from elimu_school.constant import months

# Create your models here.
# class Donation(models.Model):
    
#     donate_number = models.CharField(max_length=100)
    
#     donate_date = models.DateField()
    
#     donate_amount = models.FloatField()
    
#     reason_for_donation = models.TextField()
    
#     donate_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    
#     donate_type = models.CharField(max_length=20)
    
#     donor_name = models.CharField(max_length=50)
    
#     donor_firstname = models.CharField(max_length=50)
    
#     donor_address = models.CharField(max_length=50)
    
#     donor_postal_code = models.CharField(max_length=8)
    
#     donor_city = models.CharField(max_length=50)
    
#     donor_country = models.CharField(max_length=50)
    
#     donor_tel = models.CharField(max_length=20)
    
#     donor_email = models.CharField(max_length=120)
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"Don : {self.donor_name}"

    
# class BillingBracket(models.Model):
    
#     label = models.CharField(max_length=20)
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"Tranche de facturation : {self.label}"


# class TimeLine(models.Model):
    
#     label = models.CharField(max_length=20)
    
#     payment_month = models.CharField(max_length=20)
    
#     day_of_payment = models.CharField(max_length=20)
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"Echéancier : {self.label}"
    

# class Estimate(models.Model):
    
#     estimate_number = models.CharField(max_length=50, unique=True)
    
#     date_estimate = models.DateField()
    
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
#     career = models.ForeignKey(Career, on_delete=models.CASCADE)
    
#     item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    
#     timeline = models.ForeignKey(TimeLine, on_delete=models.DO_NOTHING)
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    
    name = models.CharField(max_length=20)
    
    default_amount = models.IntegerField(default=0)
    
    defaut_quantity = models.IntegerField(default=1)
    
    #timline_model = models.ForeignKey(TimeLine, on_delete=models.SET_NULL, null=True)
    
    is_active = models.BooleanField(default=True)
    
    #submitted_to_tranche = models.BooleanField(default=True)
    
    analytic_code = models.TextField(blank=True)
    
    school = models.ForeignKey(Etablishment, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Article : {self.name}"
    
    
class Invoice(models.Model):
    
    invoice_number = models.CharField(max_length=50, unique=True)
    
    invoice_date = models.DateField(auto_now=True)
    
    amount = models.FloatField(default=0)
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    
    schooling_of = models.CharField(max_length=10, choices=months)
    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)
    
    #timeline = models.ForeignKey(TimeLine, on_delete=models.DO_NOTHING)
    
    choices = [('Entièrement payé', 'Entièrement payé'), ('Non payé', 'Non payé'), ('Avance', 'Avance')]
    
    invoice_status = models.CharField(max_length=20, choices=choices, blank=True)
    
    is_repayment = models.BooleanField(default=False)
    
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"N°{self.invoice_number}"


class Repayment(models.Model):
    
    choices = [('Par chèque', 'Par chèque'), ('En espèce', 'En espèce')]
    repayment_method = models.CharField(max_length=20, choices=choices)
    
    amount = models.FloatField(default=0)
    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)
    
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, blank=True, null=True)
    
    repayment_date = models.DateField(auto_now=True)
    
    status = models.BooleanField(default=True)
    
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)


class FinancialCommitment(models.Model):
    
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    
    school_fees = models.IntegerField()
    
    send_date = models.DateTimeField(blank=True, null=True)
    
    is_send = models.BooleanField(default=False)
    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)

class Spend(models.Model):
    
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    
    amount = models.FloatField(default=0)
    
    comment = models.TextField(blank=True)
    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)