from django.urls import path
from . import views

urlpatterns = [
    path('', views.rain_view, name='rain'),
    path('fetch-rainfall-data/', views.fetch_rainfall_data, name='fetch_rainfall_data'),
]