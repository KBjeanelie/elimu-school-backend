from django.urls import path

from administration.views import AddUserSchoolView, IndexView, SchoolsView, AddSchoolView, UserSchoolView

app_name = 'administration'
urlpatterns = [
    path(route='', view=IndexView.as_view(), name='index'),

    path(route='établissements/', view=SchoolsView.as_view(), name='schools'),
    path(route='établissements/<int:pk>/delete/', view=SchoolsView.as_view(), name='delete_school'),
    path(route='établissements/ajouter/', view=AddSchoolView.as_view(), name='add_school'),
    
    path(route='admin-etablissement/', view=UserSchoolView.as_view(), name='user_school'),
    path(route='admin-etablissement/<int:pk>/delete/', view=UserSchoolView.as_view(), name='user_school'),
    path(route='admin-etablissement/ajouter/', view=AddUserSchoolView.as_view(), name='add_user_school'),
]
