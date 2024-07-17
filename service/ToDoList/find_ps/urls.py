from django.urls import path
from .views import password_reset_request, verify_code

urlpatterns = [
    path('', password_reset_request, name='password_reset_request'),
    path('verify/', verify_code, name='verify_code'),
]