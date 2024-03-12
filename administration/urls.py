from django.urls import path

from administration.views import AddUserSchoolView, IndexView, LoginView, SchoolsView, AddSchoolView, UserSchoolView

app_name = 'administration'
urlpatterns = [
    path(route='', view=IndexView.as_view(), name='index'),
    
    path(route='login/', view=LoginView.as_view(), name='login'),

    path(route='établissements/', view=SchoolsView.as_view(), name='schools'),
    path(route='établissements/<int:pk>/delete/', view=SchoolsView.as_view(), name='delete_school'),
    path(route='établissements/ajouter/', view=AddSchoolView.as_view(), name='add_school'),
    
    path(route='comptes-directeurs/', view=UserSchoolView.as_view(), name='user_school'),
    path(route='comptes-directeurs/<int:pk>/delete/', view=UserSchoolView.as_view(), name='user_school'),
    path(route='comptes-directeurs/ajouter/', view=AddUserSchoolView.as_view(), name='add_user_school'),
]
