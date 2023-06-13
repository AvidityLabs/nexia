
web: gunicorn code/app/core.wsgi:application --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=core.settings.dev
# worker: celery -A core worker --loglevel=info