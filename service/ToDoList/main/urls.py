from django.urls import path
from . import views
from .views import weather_view, fetch_weather_data_view

urlpatterns = [
    path('', views.map_view, name='home'),
    path('map/data/', views.map_data_view, name='map_data'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('waterlevel/', views.waterlevel, name='waterlevel'), 
    path('handle_button/', views.handle_button, name='handle_button'),
    path('delete/', views.delete_account, name='delete_account'),  # 회원 탈퇴 URL
    path('profile/', views.profile, name='profile'), 
    path('edit_profile/', views.edit_profile, name='edit_profile'),# 내 정보 조회 URL
    path('detect/', views.detect, name='detect'),
    path('weather/', weather_view, name='weather_view'),
    path('api/weather/', fetch_weather_data_view, name='fetch_weather_data_view'),

]