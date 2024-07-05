from django.urls import path
from .views import rain_view

urlpatterns = [
    path('', rain_view, name='rain_view'),
]