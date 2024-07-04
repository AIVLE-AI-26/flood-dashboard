from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('sighup/', include('sighup.urls')),  # sighup 경로로 수정
    path('login/', include('login.urls')),
]