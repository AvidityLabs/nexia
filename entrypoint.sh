#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done

    echo "MYSQL started"
fi


python manage.py flush --no-input --settings=code/app/core.settings.dev

# Check if migrations are needed
python manage.py makemigrations --dry-run --check --code/app/settings=core.settings.dev > /dev/null 2>&1
MIGRATIONS_NEEDED=$?

if [ $MIGRATIONS_NEEDED -eq 0 ]; then
    # Migrations needed, apply them
    python manage.py makemigrations --settings=code/app/core.settings.dev
    python manage.py migrate --settings=code/app/core.settings.dev
fi

# Check if superuser needs to be created
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists()" --settings=code/app/core.settings.dev | grep "False" > /dev/null 2>&1
SUPERUSER_EXISTS=$?

if [ $SUPERUSER_EXISTS -eq 0 ]; then
    # Superuser does not exist, create it
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')" | python manage.py shell --settings=code/app/core.settings.dev
fi

# Start the Gunicorn server
# gunicorn code/app/core.wsgi:application --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=code/app/core.settings.dev

# unlink /etc/nginx/sites-enabled/default

# nginx -g  'daemon off;'
