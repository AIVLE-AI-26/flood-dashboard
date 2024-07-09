from django.urls import path
from . import views

urlpatterns = [
    path('', views.waterlevel, name='waterlevel'),
    path('data/', views.get_waterlevel_data, name='get_waterlevel_data'),
]