from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='home'),
    path('map/data/', views.map_data_view, name='map_data'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('waterlevel/', views.waterlevel, name='waterlevel'), 
    path('handle_button/', views.handle_button, name='handle_button'),
]