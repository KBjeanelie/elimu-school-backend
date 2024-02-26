from django.urls import path
from backend.views import LoginView, LogoutView

app_name = 'backend'
urlpatterns = [
    path('login/', view=LoginView.as_view(), name="login"),
    path('logout/', view=LogoutView.as_view(), name="logout")
]
