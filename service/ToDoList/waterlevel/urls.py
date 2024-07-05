from django.urls import path
from . import views

urlpatterns = [
    path('', views.waterlevel_view, name='waterlevel'),
]