from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='detect_home'),
    path('upload/', views.upload_image, name='upload_image'),
]
