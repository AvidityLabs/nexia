# coding: utf-8
from .base import *



INSTALLED_APPS += ['debug_toolbar']

PAYPAL_TEST = True
# SECURITY WARNING: keep the secret key used in production secret!


# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
    # 'http://127.0.0.1:3000'
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = ['*']

CORS_ALLOW_HEADERS = [
    'Accept',
    'Accept-Language',
    'Content-Type',
    'Authorization',
    'Content-Type',
    # Add any additional headers your API requires
]



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "api"
    }
}

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django_psdb_engine',
        'NAME': config('DB_NAME'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'OPTIONS': {
            'ssl': {'ca': BASE_DIR / config('MYSQL_ATTR_SSL_CA')},
            'charset': 'utf8mb4'
        }
    }
}





INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


# Broker

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"


# EMAIL
EMAIL_USE_TLS = True
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = 2525
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# MPESA
MPESA_SHORTCODE_TYPE = config('MPESA_SHORTCODE_TYPE')
MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY')
MPESA_INITIATOR_USERNAME = config('MPESA_INITIATOR_USERNAME')
MPESA_ENVIRONMENT = config('MPESA_ENVIRONMENT')
MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = config('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = config('MPESA_SHORTCODE')
MPESA_EXPRESS_SHORTCODE = config('MPESA_EXPRESS_SHORTCODE')
MPESA_SHORTCODE_TYPE = config('MPESA_SHORTCODE_TYPE')
MPESA_PASSKEY = config('MPESA_PASSKEY')
MPESA_INITIATOR_USERNAME = config('MPESA_INITIATOR_USERNAME')
MPESA_INITIATOR_SECURITY_CREDENTIAL = config('MPESA_INITIATOR_SECURITY_CREDENTIAL')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
DISABLE_COLLECTSTATIC = 1
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# DISABLE_COLLECTSTATIC = 0
# media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
