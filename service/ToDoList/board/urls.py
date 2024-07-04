from django.urls import path
from . import views

urlpatterns = [
    path('write/', views.board_write, name='board_write'),
    path('list/', views.board_list, name='board_list'),
]