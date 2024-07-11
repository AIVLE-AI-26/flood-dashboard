from django.urls import path
from . import views

urlpatterns = [
    path('', views.terms_view, name='terms'),
]