from django.urls import path
from accountant_dashboard.views.administration_view import AddItemView, EditItemView, EditProfileView, ItemView, ProfileAppView
from accountant_dashboard.views.communication_view import EventsView, InformationsView
from accountant_dashboard.views.facture_comptable_view import AddDepenseView, AddInvoiceView, AddRepaymentView, BalanceMonitoring, DepenseView, EditDepenseView, EditInvoiceView, EditRepaymentView, FinancialCommitmentView, InvoiceDetailView, InvoiceView, RepaymentView
from accountant_dashboard.views.home_view import AccountantIndexView, NotAcademicYearFound, PreRegistrationDetailView, PreRegistrationView


app_name = 'accountant_dashboard'
urlpatterns = [
    path(route="", view=AccountantIndexView.as_view(), name="index"),
    path(route='gestion_universite/demande-de-préinscription/', view=PreRegistrationView.as_view(), name='pre_registrations'),
    path(route='gestion_universite/demande-de-préinscription/<int:pk>/detail/', view=PreRegistrationDetailView.as_view(), name='pre_registrations_detail'),
    path(route='gestion_universite/demande-de-préinscription/<int:pk>/check/', view=PreRegistrationDetailView.check, name='pre_registrations_check'),
    path(route='gestion_universite/demande-de-préinscription/<int:pk>/delete/', view=PreRegistrationDetailView.delete, name='pre_registrations_delete'),
    
    
    path(route='communication/infomations/', view=InformationsView.as_view(), name='infos'),
    path(route='communication/evenements/', view=EventsView.as_view(), name='events'),
    
    path(route='administration/articles/', view=ItemView.as_view(), name='items'),
    path(route='administration/articles/ajouter/', view=AddItemView.as_view(), name='add_item'),
    path(route='administration/articles/<int:pk>/editer/', view=EditItemView.as_view(), name='edit_item'),
    path(route='administration/articles/<int:pk>/delete/', view=ItemView.as_view(), name='delete_item'),
    path(route='administration/user-profile/', view=ProfileAppView.as_view(), name='user_profile'),
    path(route='administration/user-profile/edit/', view=EditProfileView.as_view(), name='edit_profil'),
    
    path(route='factures-&-comptable/factures/', view=InvoiceView.as_view(), name='invoices'),
    path(route='factures-&-comptable/factures/<int:pk>/detail/', view=InvoiceDetailView.as_view(), name='invoice'),
    path(route='factures-&-comptable/factures/ajouter/', view=AddInvoiceView.as_view(), name='invoice_add'),
    path(route='factures-&-comptable/factures/<int:pk>/editer/', view=EditInvoiceView.as_view(), name='invoice_edit'),
    path(route='factures-&-comptable/factures/<int:pk>/delete/', view=InvoiceView.as_view(), name='delete_invoice'),
    
    path(route='factures-&-comptable/remboursements/', view=RepaymentView.as_view(), name='repayments'),
    path(route='factures-&-comptable/remboursements/ajouter/', view=AddRepaymentView.as_view(), name='add_repayment'),
    path(route='factures-&-comptable/remboursements/<int:pk>/editer/', view=EditRepaymentView.as_view(), name='edit_repayment'),
    path(route='factures-&-comptable/remboursements/<int:pk>/delete/', view=RepaymentView.as_view(), name='delete_repayment'),
    
    path(route='factures-&-comptable/rapport-des-depenses/', view=DepenseView.as_view(), name='spend'),
    path(route='factures-&-comptable/rapport-des-depenses/ajouter/', view=AddDepenseView.as_view(), name='add_spend'),
    path(route='factures-&-comptable/rapport-des-depenses/<int:pk>/editer/', view=EditDepenseView.as_view(), name='edit_spend'),
    path(route='factures-&-comptable/rapport-des-depenses/<int:pk>/delete/', view=DepenseView.as_view(), name='delete_spend'),
    
    path(route='factures-&-comptable/engagement-financier/', view=FinancialCommitmentView.as_view(), name='financials'),
    path(route='factures-&-comptable/engagement-financier/<int:pk>/send/', view=FinancialCommitmentView.send, name='send_financials'),
    
    path(route='rapport-financier/suivis-des-soldes/', view=BalanceMonitoring.as_view(), name='balances'),
    
    path(route='no-academic-year-found/', view=NotAcademicYearFound.as_view(), name='no_year'),
    
]
