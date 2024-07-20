from pathlib import Path
import os
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-^bdpx&4fa9(pi&1431q$$cq132vorhqc#kga%)%au3%f&6@=)+"

DEBUG = True

ALLOWED_HOSTS = []

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'chatbot',  # 챗봇 안 쓰면 비활성화
    'signup',
    'login',
    'board',
    'rain',
    'terms',
    'detect',
    'find_username',
    'find_ps',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ToDoList.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ToDoList.wsgi.application"

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'main/static'),
    os.path.join(BASE_DIR, 'chatbot/static'),
    os.path.join(BASE_DIR, 'signup/static'),
    os.path.join(BASE_DIR, 'login/static'),
    os.path.join(BASE_DIR, 'rain/static'),
    os.path.join(BASE_DIR, 'waterlevel/static'),
    os.path.join(BASE_DIR, 'terms/static'),
    os.path.join(BASE_DIR, 'detect/static'),
    os.path.join(BASE_DIR, 'find_username/static'),
    os.path.join(BASE_DIR, 'find_ps/static'),
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATA_DIR = os.path.join(BASE_DIR, 'data')

X_FRAME_OPTIONS = 'SAMEORIGIN'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'wateravle26@gmail.com'  # 실제 이메일 주소
EMAIL_HOST_PASSWORD = 'z v q p k x c k j y w s u h s i'  # 실제 이메일 계정의 비밀번호 또는 앱 비밀번호
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 실제 이메일 주소

AUTHENTICATION_BACKENDS = [
    'signup.backends.CustomUserBackend',  # CustomUserBackend의 실제 경로로 변경
    'django.contrib.auth.backends.ModelBackend',  # 기본 인증 백엔드
]


AUTH_USER_MODEL = 'signup.CustomUser'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 기본값
SESSION_COOKIE_AGE = 1200  # 세션 쿠키 만료 시간 (초), 필요에 따라 조정
SESSION_SAVE_EVERY_REQUEST = True  # 매 요청마다 세션 갱신
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 브라우저 닫을 때 세션 만료