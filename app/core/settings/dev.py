# coding: utf-8
from .base import *
import dj_database_url


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
DATABASES = {'default': dj_database_url.config(default=config('DATABASE_URL'))}
DATABASES['default']["ATOMIC_REQUESTS"] = True
DATABASES['default']["CONN_MAX_AGE"] = 60




INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


# Broker

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"







# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
DISABLE_COLLECTSTATIC = 1
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# DISABLE_COLLECTSTATIC = 0
# media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
