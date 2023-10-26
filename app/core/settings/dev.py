# coding: utf-8
from .base import *
import dj_database_url


INSTALLED_APPS += ['debug_toolbar']

PAYPAL_TEST = True
# SECURITY WARNING: keep the secret key used in production secret!

ALLOWED_HOSTS = ['localhost','127.0.0.1']
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'https://andika.pro',
    'http://localhost:4200'
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

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
# Check if the DATABASE_URL environment variable is set and not empty
# if 'DATABASE_URL' in os.environ and os.environ['DATABASE_URL']:
#     # Use the configured database URL
#     DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}
# else:
#     # Use SQLite as a fallback if DATABASE_URL is not set or empty
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django_psdb_engine',
#         'NAME': os.environ.get('DB_NAME'),
#         'HOST': os.environ.get('DB_HOST'),
#         'PORT': os.environ.get('DB_PORT'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'OPTIONS': {'ssl': {'ca': os.environ.get('MYSQL_ATTR_SSL_CA')}, 'charset': 'utf8mb4'}
#     }
# }
# Enable atomic requests and set connection max age
# DATABASES['default']["ATOMIC_REQUESTS"] = True
# DATABASES['default']["CONN_MAX_AGE"] = 60



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
