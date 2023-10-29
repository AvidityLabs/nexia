"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from pathlib import Path
import os
from decouple import config

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = config('DEBUG', cast=bool)

SECRET_KEY = config('SECRET_KEY')

#TODO Apparently this is not being reused on other settings
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(",")

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Signal Configs
    # Applications
    'api.APIAppConfig',
    'social_auth',
    'payments',
    'usecases',
    'documents',
    # Third party libraries
    "whitenoise.runserver_nostatic",
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'django_filters',
    'cloudinary',
    'paypal.standard.ipn',
    'llm.apps.LlmConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'api.exceptions.handle_500.InternalServerErrorMiddleware',
    'api.exceptions.handle_404.Handle404Middleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


AUTH_USER_MODEL = 'api.User'


REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.exceptions.responses.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.backends.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Nexia API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}


ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}






EMOTION_MODEL_TOKEN = config('EMOTION_MODEL_TOKEN')
EMOTION_MODEL_URL = config('EMOTION_MODEL_URL')
SENTIMENT_MODEL_URL = config('SENTIMENT_MODEL_URL')
SENTIMENT_MODEL_TOKEN = config('SENTIMENT_MODEL_TOKEN')
STABLE_DIFFUSION_API_KEY = config('STABLE_DIFFUSION_API_KEY')
OPENAI_API_KEY = config('OPENAI_API_KEY')
OPENAI_ORGANIZATION = config('OPENAI_ORGANIZATION')

# Social e.g google ,witter etc
SOCIAL_SECRET = config('SOCIAL_SECRET')

# FireBase
FIREBASE_CLIENT_ID = config('FIREBASE_CLIENT_ID')
FIREBASE_AUTH_URI = config('FIREBASE_AUTH_URI')
FIREBASE_TOKEN_URI = config('FIREBASE_TOKEN_URI')
FIREBASE_TOKEN_URI_AUTH_PROVIDER_X_509_CERT_URL = config('FIREBASE_TOKEN_URI_AUTH_PROVIDER_X_509_CERT_URL')

# EMAIL 
EMAIL_USE_TLS = True
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = 2525
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_CONFIRMATION_URL = config('EMAIL_CONFIRMATION_URL')
EMAIL_FROM = config('EMAIL_FROM')

# MPESA
MPESA_ENVIRONMENT = config('MPESA_ENVIRONMENT')
MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = config('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = config('MPESA_SHORTCODE')
MPESA_EXPRESS_SHORTCODE = config('MPESA_EXPRESS_SHORTCODE')
MPESA_SHORTCODE_TYPE = config('MPESA_SHORTCODE_TYPE')
MPESA_PASSKEY = config('MPESA_PASSKEY')
MPESA_INITIATOR_USERNAME = config('MPESA_INITIATOR_USERNAME')
MPESA_INITIATOR_SECURITY_CREDENTIAL = config('MPESA_INITIATOR_SECURITY_CREDENTIAL')
