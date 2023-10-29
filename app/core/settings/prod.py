
from .base import *


import sentry_sdk
import cloudinary
import cloudinary.uploader
import cloudinary.api
from kombu import Queue
from sentry_sdk.integrations.django import DjangoIntegration

# import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
envpath = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=envpath)

sentry_sdk.init(
    dsn="https://662de0da1df04ff98e2fd61461518edb@o333282.ingest.sentry.io/4505043740327936",
    integrations=[
        DjangoIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


DEBUG = int(os.environ.get("DEBUG", default=0))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PAYPAL_TEST = True
# SECURITY WARNING: keep the secret key used in production secret!



# Enable HTTPS-only communication for a specified amount of time, with subdomains included
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds
# Redirect all non-HTTPS requests to HTTPS
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_PRELOAD = True

# CSRF_TRUSTED_ORIGINS = ['https://*.fly.dev']


ALLOWED_HOSTS = ['*'] #TODO fix this
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
    'andika.applikuapp.com'
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


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "api"
    }
}

# Broker

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

# TODO decouple settings.py into dev, staging and prod
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

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
DISABLE_COLLECTSTATIC = 1
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# DISABLE_COLLECTSTATIC = 0
# media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"


cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'human_readable': {
#             'format': '[%(asctime)s] %(levelname)s %(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'human_readable',
#             'level': 'DEBUG',
#         },
#         'file': {
#             'class': 'logging.FileHandler',
#             'filename': 'nexia.log',
#             'formatter': 'human_readable',
#             'level': 'INFO',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file'],
#             'level': 'INFO',
#         },
#     },
# }


# EMAIL
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# MPESA
MPESA_SHORTCODE_TYPE = os.environ.get('MPESA_SHORTCODE_TYPE')
MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
MPESA_INITIATOR_USERNAME = os.environ.get('MPESA_INITIATOR_USERNAME')
MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT')
MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE')
MPESA_EXPRESS_SHORTCODE = os.environ.get('MPESA_EXPRESS_SHORTCODE')
MPESA_SHORTCODE_TYPE = os.environ.get('MPESA_SHORTCODE_TYPE')
MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY')
MPESA_INITIATOR_USERNAME = os.environ.get('MPESA_INITIATOR_USERNAME')
MPESA_INITIATOR_SECURITY_CREDENTIAL = os.environ.get('MPESA_INITIATOR_SECURITY_CREDENTIAL')
