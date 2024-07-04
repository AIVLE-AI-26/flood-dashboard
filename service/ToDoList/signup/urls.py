from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
]