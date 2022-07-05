import os
from kombu import Queue, Exchange
"""
Django settings for cockpit project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p52hpr)1r*8!!392&w6d-$*_5+7nas=o0o$4zqhr1f62a3rk7y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guacamole.apps.GuacamoleConfig',
    'platforms.apps.PlatformsConfig',
    'user.apps.UserConfig',
    'k8s.apps.K8SConfig'
]

MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:4200',
# ] # If this is used, then not need to use `CORS_ALLOW_ALL_ORIGINS = True`
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     'http://localhost:4200',
# ]

ROOT_URLCONF = 'cockpit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cockpit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'guacamole_db':{
        'NAME':         os.getenv("GUACAMOLE_DB_NAME","guacamole_db"),       #'guacamole_db',
        'ENGINE':       'django.db.backends.postgresql',
        'USER':         os.getenv("GUACAMOLE_DB_USER","guacamole_user"),
        'PASSWORD':     os.getenv("GUACAMOLE_DB_PASSWORD","dd0aa4251547c12c941cde21"),
        'HOST':         os.getenv("GUACAMOLE_DB_HOST",'guacamole_pg'),
        'PORT':         os.getenv("GUACAMOLE_DB_PORT",'5432'),
    },
    'default':{
        'NAME':         os.getenv("PLATFORM_DB_NAME","platform_db"),       #'platform_db',
        'ENGINE':       'django.db.backends.postgresql',
        'USER':         os.getenv("PLATFORM_DB_USER","platform_user"),
        'PASSWORD':     os.getenv("PLATFROM_DB_PASSWORD","e8bfc3e6d12443830116b721"),
        'HOST':         os.getenv("PLATFORM_DB_HOST",'platform_pg'),
        'PORT':         os.getenv("PLATFORM_DB_PORT",'5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#DB Routers
#DATABASE_ROUTERS = ['platforms.dbrouters.PlatformsRouter','guacamole.dbrouters.GuacamoleRouter']

CELERY_BROKER_URL =  os.getenv("MESSAGE_BROKER_URL","amqp://guest@localhost:5672")                   #'amqp://localhost' #env
#CELERY_RESULT_BACKEND = "amqp"         #env
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
CELERY_AMQP_TASK_RESULT_EXPIRES = 1000
CELERY_IMPORTS=['guacamole.guacamole_utils','platforms.platform_utils',]
CELERY_TASK_CREATE_MISSING_QUEUES=True
CELERY_CREATE_MISSING_QUEUES = True
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('guacamole', Exchange('guacamole'), routing_key='long_tasks'),
)
CELERY_ROUTES = {
    'guacamole.guacamole_utils.*': {
        'queue': 'guacamole',
        'routing_key': 'long_tasks',
    },
}

# #############EMAIL_SETTINGS #########
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL=os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')#'your_account@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')#'your accounts password'

