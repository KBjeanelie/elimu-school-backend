import datetime
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from backend.forms.facturation_forms import InvoiceForm, RepaymentForm, SpendForm
from backend.models.facturation import FinancialCommitment, Invoice, Repayment, Spend
from django.core.cache import cache
from django.db.models import Sum
from django.contrib import messages
from backend.models.gestion_ecole import AcademicYear

def generate_payment_number():
        now = datetime.datetime.now()
        year = now.year
        # Utilisation du cache pour stocker le compteur
        regulation_counter = cache.get('regulation_counter') or 0
        regulation_counter += 1
        cache.set('regulation_counter', regulation_counter)

        return f"REGL{year}{regulation_counter}"
    
def generate_invoice_number():
        now = datetime.datetime.now()
        year = now.year
        # Utilisation du cache pour stocker le compteur
        invoice_counter = cache.get('invoice_counter') or 0
        invoice_counter += 1
        cache.set('invoice_counter', invoice_counter)
        
        return f"FA{year}{invoice_counter}"


class FinancialCommitmentView(View):
    template_name = "accountant_dashboard/facture_comp/engagement_financier.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        engagements = FinancialCommitment.objects.filter(academic_year=academic_year)
        context = {'engagements':engagements}
        return render(request, template_name=self.template_name, context=context)
    
    def send(self, pk, *args, **kwargs):
        engagement = FinancialCommitment.objects.get(pk=pk)
        engagement.send_date = now()
        engagement.is_send = True
        engagement.save()
        #messages.success(request, "Engagement financier envoyé avec succès !")
        return redirect('accountant_dashboard:financials')
        

class InvoiceView(View):
    template_name = "accountant_dashboard/facture_comp/factures.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        invoices = Invoice.objects.filter(academic_year=academic_year)
        form = InvoiceForm(request.user,)
        context = {'invoices':invoices, 'form':form}
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        form = InvoiceForm(request.user, request.POST)
        if form.is_valid():
            invoice_number = generate_invoice_number()
            career = form.cleaned_data['career']
            item = form.cleaned_data['item']
            amount = form.cleaned_data['amount']
            student = form.cleaned_data['student']
            comment = form.cleaned_data['comment']
            invoice_status = form.cleaned_data['invoice_status']
            
            # Utilisation des valeurs récupérées pour créer une nouvelle instance de la facture
            invoice = Invoice(
                invoice_number=invoice_number,
                career=career,
                item=item,
                amount=amount,
                student=student,
                comment=comment,
                invoice_status=invoice_status,
                academic_year=academic_year
            )
            invoice.save()
            messages.success(request, "La facture a été enregistré avec succès !")
            return redirect("accountant_dashboard:invoices")
        
        messages.error(request, "ERREUR : Impossible d'ajouter la facture !")
        return redirect("accountant_dashboard:invoices")
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Invoice, pk=pk)
        instance.delete()
        
        invoices = Invoice.objects.all().order_by('-created_at')
        context = {'invoices':invoices}
        return render(request, template_name=self.template_name, context=context)

class InvoiceDetailView(View):
    template_name = "accountant_dashboard/facture_comp/facture-info.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk)
        context = {'invoice':invoice}
        return render(request, template_name=self.template_name, context=context)


class EditInvoiceView(View):
    template_name = "accountant_dashboard/facture_comp/edit_facture.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request,pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk)
        form = InvoiceForm(request.user, instance=invoice)
        context = {'invoice':invoice, 'form':form}
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceForm(request.user, request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, "La facture a été modifier avec succès !")
            return redirect("accountant_dashboard:invoices")
        
        messages.error(request, "ERREUR : Impossible de modifier la facture !")
        context = {'invoice':invoice, 'form':form}
        return render(request, template_name=self.template_name, context=context)


#=============================== PARTIE CONCERNANT LES REMBOURSEMENTS ==========================
class EditRepaymentView(View):
    template = "accountant_dashboard/facture_comp/editer_remboursement.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, pk, *args, **kwargs):
        repayment = get_object_or_404(Repayment, pk=pk)
        form = RepaymentForm(request.user, instance=repayment)
        context = {'form':form, 'repayment':repayment}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        repayment = get_object_or_404(Repayment, pk=pk)
        data = request.POST.copy()
        data['academic_year'] = academic_year
        invoice = Invoice.objects.get(academic_year=academic_year, pk=data['invoice'])
        data['amount'] = invoice.amount
        form = RepaymentForm(request.user, data, instance=repayment)
        if form.is_valid():
            form.save()
            messages.success(request, "Remousement a été modifier avec succès !")
            return redirect('accountant_dashboard:repayments')
        
        messages.error(request, "ERROR: Something went wrong, please try again !")
        context = {'form': form, 'repayment': repayment}
        return render(request, template_name=self.template, context=context)
    
class AddRepaymentView(View):
    template = "accountant_dashboard/facture_comp/ajout_remboursement.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = RepaymentForm(request.user)
        context = {'form':form}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, *args, **kwargs):
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        data = request.POST.copy()
        data['academic_year'] = academic_year
        invoice = Invoice.objects.get(academic_year=academic_year, pk=data['invoice'])
        data['amount'] = invoice.amount
        form = RepaymentForm(request.user, data)
        if form.is_valid():
            form.save()
            invoice.is_repayment = True
            invoice.save()
            messages.success(request, "La facture a été remboursé avec succès !")
            return redirect("accountant_dashboard:repayments")
        
        messages.error(request, "ERREUR: Impossible de remboursé la facture :(")
        context = {'form':form}
        return render(request, template_name=self.template, context=context)

class RepaymentView(View):
    template = "accountant_dashboard/facture_comp/remboursements.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        repayments = Repayment.objects.filter(academic_year=academic_year).order_by('-created_at')
        context = {'repayments': repayments}
        return render(request, template_name=self.template, context=context)
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Repayment, pk=pk)
        instance.invoice.is_repayment = False
        instance.invoice.save()
        instance.delete()
        
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        repayments = Repayment.objects.filter(academic_year=academic_year).order_by('-created_at')
        context = {'repayments': repayments}
        return render(request, template_name=self.template, context=context)
    
#===END

class DepenseView(View):
    template_name = "accountant_dashboard/rapport_financier/depenses.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        spends = Spend.objects.filter(academic_year=academic_year).order_by('-created_at')
        context = {'spends':spends}
        return render(request, template_name=self.template_name, context=context)
    
    def delete(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Spend, pk=pk)
        instance.delete()
        
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        spends = Spend.objects.filter(academic_year=academic_year).order_by('-created_at')
        context = {'spends':spends}
        return render(request, template_name=self.template_name, context=context)
    

class AddDepenseView(View):
    template = "accountant_dashboard/rapport_financier/ajout_depense.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = SpendForm(request.user)
        context = {'form':form}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        data['academic_year'] = academic_year
        form = SpendForm(request.user, data)
        if form.is_valid():
            form.save()
            messages.success(request, "Dépense a été enregistré avec succès !")
            return redirect("accountant_dashboard:spend")
        
        messages.error(request, "ERREUR: Impossible d'ajouter une dépense !")
        context = {'form':form}
        return render(request, template_name=self.template, context=context)

class EditDepenseView(View):
    template = "accountant_dashboard/rapport_financier/editer_depense.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, pk, *args, **kwargs):
        spend = Spend.objects.get(pk=pk)
        form = SpendForm(request.user, instance=spend)
        context = {'form':form}
        return render(request, template_name=self.template, context=context)
    
    def post(self, request, pk, *args, **kwargs):
        data = request.POST.copy()
        spend = Spend.objects.get(pk=pk)
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        data['academic_year'] = academic_year
        form = SpendForm(request.user, data, instance=spend)
        if form.is_valid():
            form.save()
            messages.success(request, "Dépense a été modifier avec succès !")
            return redirect("accountant_dashboard:spend")
        
        messages.error(request, "ERREUR: Impossible de modifier une dépense !")
        context = {'form':form}
        return render(request, template_name=self.template, context=context)


class BalanceMonitoring(View):
    template_name = "accountant_dashboard/rapport_financier/suivi_solde.html"
    
    def dispatch(self,request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('backend:login')
        
        if not request.user.is_accountant:
            return redirect('backend:logout')
        try:
            active_year = AcademicYear.objects.get(status=True, school=request.user.school)
        except AcademicYear.DoesNotExist:
            return redirect('accountant_dashboard:no_year')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        #recuperer l'ensemble des facture déjà totalement payé
        academic_year = AcademicYear.objects.get(school=request.user.school, status=True)
        invoices = Invoice.objects.filter(academic_year=academic_year, invoice_status='Entièrement payé', is_repayment=False).order_by('-created_at')

        #recuperer le nombre total de facture payé
        count_invoices = Invoice.objects.filter(academic_year=academic_year, invoice_status='Entièrement payé', is_repayment=False).count()
        
        # Somme des montants des factures payées
        amount_payed = invoices.aggregate(total_montant=Sum('amount'))['total_montant'] or 0

        # Récupérer tous les engagements financiers
        engagements = FinancialCommitment.objects.filter(academic_year=academic_year)
        total_engagements = engagements.aggregate(total=Sum('school_fees'))['total'] or 0

        # Calcul du montant impayé
        not_payed = total_engagements - amount_payed

        context = {
            'invoices':invoices,
            'count_invoices':count_invoices,
            'amount_payed':amount_payed,
            'total_engagements':total_engagements,
            'not_payed':not_payed
        }
        return render(request, template_name=self.template_name, context=context)


