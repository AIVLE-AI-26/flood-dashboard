from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('chatbot/', include('chatbot.urls')),  # 챗봇 안쓰면 비활성화
    path('signup/', include('signup.urls')),  # sighup 경로로 수정
    path('login/', include('login.urls')),
    path('board/', include('board.urls')),
    path('rain/', include('rain.urls')),
    path('waterlevel/', include('waterlevel.urls')),
    path('terms/', include('terms.urls')),
    path('detect/', include('detect.urls')),
    path('find_username/', include('find_username.urls')),
    path('find-password/', include('find_ps.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
