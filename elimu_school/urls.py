"""elimu_school URL Configuration """
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from api.views.user_account_view import LoginAPIView, LogoutAPIView
from elimu_school import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='ELIMU API')
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    
    path('', include('administration.urls')),
    path('manager_dashboard/', include('manager_dashboard.urls')),
    path('accountnant-dashboard/', include('accountant_dashboard.urls')),
    path('authentication/', include('backend.urls')),
    
    path('admin/', admin.site.urls),
    
    re_path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
