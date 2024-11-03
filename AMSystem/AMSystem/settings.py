"""
Django settings for AMSystem project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
<<<<<<< HEAD
import os
=======

>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

<<<<<<< HEAD
=======

>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=creds)y8n8cm*s^#94miq+mz!*ico7he37&gb5o0u%pa-53e-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

<<<<<<< HEAD
# Application definition

INSTALLED_APPS = [
    'unfold',
=======

# Application definition

INSTALLED_APPS = [
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
<<<<<<< HEAD
    'attendance',
    'dashboard',
    'userauth',
    'usermgmt',
    'django_browser_reload',
=======
    'userauth',
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
<<<<<<< HEAD
    'django.contrib.sessions.middleware.SessionMiddleware',  # Ensure this is before CsrfViewMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Ensure this is after SessionMiddleware
=======
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

<<<<<<< HEAD
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # This is the default
)

=======
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
ROOT_URLCONF = 'AMSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
<<<<<<< HEAD
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Ensure this points to your templates directory
=======
        'DIRS': [],
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
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

WSGI_APPLICATION = 'AMSystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
<<<<<<< HEAD
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
=======

STATIC_URL = 'static/'
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

<<<<<<< HEAD
NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'

AUTH_USER_MODEL = 'usermgmt.User'

LOGIN_URL = 'login'

# Use database-backed sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Optionally set the session to expire when the browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600  # 1 hour for testing; adjust as necessary

# CSRF settings
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_USE_SESSIONS = True
=======
NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
