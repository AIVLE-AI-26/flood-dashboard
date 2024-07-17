from django.urls import path
from .views import find_username

urlpatterns = [
    path('', find_username, name='find_username'),
]