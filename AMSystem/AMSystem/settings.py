"""
Django settings for AMSystem project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=creds)y8n8cm*s^#94miq+mz!*ico7he37&gb5o0u%pa-53e-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.import_export',
    'unfold.contrib.filters',
    'django_light',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'import_export',
    'attendance',
    'dashboard',
    'userauth',
    'management',
    'leave',
    'django_browser_reload',
    'django_apscheduler',
    'rest_framework',
]


# ===================
# MIDDLEWARE
# ===================
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===================
# URL CONFIGURATION
# ===================
ROOT_URLCONF = 'AMSystem.urls'


# ===================
# TEMPLATES
# ===================
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', 
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Ensure this points to your templates directory
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


# ===================
# WSGI APPLICATION
# ===================
WSGI_APPLICATION = 'AMSystem.wsgi.application'


# ===================
# DATABASES
# ===================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ===================
# AUTHENTICATION
# ===================

AUTH_USER_MODEL = 'management.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

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


# ===================
# INTERNATIONALIZATION
# ===================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Singapore'
USE_I18N = True
USE_TZ = True


# ===================
# STATIC FILES
# ===================
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# ===================
# DEFAULT PRIMARY KEY FIELD TYPE
# ===================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===================
# TAILWIND SETTINGS
# ===================
TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = 'C:/Program Files/nodejs/npm.cmd'


# ===================
# INTERNALS
# ===================
INTERNAL_IPS = [
    "127.0.0.1",
]

LOGIN_URL = 'userauth:login'
LOGOUT_REDIRECT_URL = 'userauth:login'


# ===================
# SESSION SETTINGS
# ===================
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 120  

# CSRF settings
# CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
# CSRF_USE_SESSIONS = True


# ===================
# UNFOLD CONFIG
# ===================

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


UNFOLD = {
    "SITE_TITLE": "AMSystem",
    "SITE_HEADER": "AMSystem",
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    "SITE_ICON": {
        "light": lambda request: static("images/AMSystemlogo-dark.png"),  # light mode
        "dark": lambda request: static("images/AMSystemlogo-light.png"),  # dark mode
    },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    "SITE_LOGO": {
        "light": lambda request: static("images/AMSystemlogo-dark.png"),  # light mode
        "dark": lambda request: static("images/AMSystemlogo-light.png"),  # dark mode
    },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("images/AMSystemlogoWhite.png"),
        },
    ],
    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True

    # "THEME": "dark", # Force theme: "dark" or "light". Will disable theme switcher


    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "badge": "Main Admin",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Departments"),
                        "icon": "Groups",  # Supported icon set: https://fonts.google.com/icons
                        # "user": lambda request: static("images/adduser.png"),
                        "link": reverse_lazy("admin:management_department_changelist"),
                        "badge": "Add Groups",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Roles"),
                        "icon": "Group",  # Supported icon set: https://fonts.google.com/icons
                        # "user": lambda request: static("images/adduser.png"),
                        "link": reverse_lazy("admin:management_role_changelist"),
                        "badge": "Add Role",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Users"),
                        "icon": "Person",  # Supported icon set: https://fonts.google.com/icons
                        # "user": lambda request: static("images/adduser.png"),
                        "link": reverse_lazy("admin:management_user_changelist"),
                        "badge": "Add Users",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    
                ],
            },
        ],
    },
}
