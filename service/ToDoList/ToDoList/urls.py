from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    # path('chatbot/', include('chatbot.urls')),
    path('signup/', include('signup.urls')),  # sighup 경로로 수정
    path('login/', include('login.urls')),
    path('board/', include('board.urls')),
    path('rain/', include('rain.urls')),
    path('waterlevel/', include('waterlevel.urls')),
    
]