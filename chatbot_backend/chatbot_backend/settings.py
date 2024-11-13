import os
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'chatbot_api',
]
SECRET_KEY = get_random_secret_key()

STATIC_URL = '/static/'

ALLOWED_HOSTS = ['*', '127.0.0.1', 'localhost']
DEBUG = True

ROOT_URLCONF = 'chatbot_backend.urls'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',  # E410 해결
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # E408 해결
    'django.contrib.messages.middleware.MessageMiddleware',  # E409 해결
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # 템플릿 파일 경로를 추가할 수 있습니다.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
