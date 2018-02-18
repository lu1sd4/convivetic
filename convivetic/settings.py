"""
Django settings for convivetic project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9u7ysc$0@*&m*n319=)ea^#+lwz$erc=ebl0rd9kg=4zb7ep*@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '192.168.1.69']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'convivetic.urls'

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

WSGI_APPLICATION = 'convivetic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

ENV_PATH = os.path.abspath(os.path.dirname(__file__))

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(ENV_PATH,'media/')
MEDIA_URL = 'media/'

# Auth options

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# Email verification

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'convivetic.e@gmail.com'
EMAIL_HOST_PASSWORD = 'y72rsQ8z'
EMAIL_PORT = 587

# For YouTube uploads

# YouTube app

CLIENT_ID = '367931440425-7d9ukeoek3s1pacp66f4ou9vvgds0lk9.apps.googleusercontent.com'
CLIENT_SECRET = 'pUC0H5AH9S7oIjCpPOXUBmcf'
SCOPE = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.photos.readonly https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/drive.scripts https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.upload'
API_KEY = 'AIzaSyA6hCsmPkcjbcWNHqrXAR-7KHHwN92ONLk'

# User creds

REFRESH_TOKEN = '1/fOJ7MVeJzeYNbym_6Qwsrkh5Fim2LtXIdtVBLwyKjy4'
ACCESS_TOKEN = 'ya29.GlxABaTlnqWLvABrhPqNv6UtAMcAoKd2lp0IZeUxTcGup29kRA59WUxlmSXOew4L6nxkUD90-10wd1Xunvdn79pnk8jrwtSkLeHX1VBsIDheXoRFVeUulbfXL4HAmQ'