#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done

    echo "MYSQL started"
fi

python manage.py flush --no-input

# Check if migrations are needed
python manage.py makemigrations --dry-run --check > /dev/null 2>&1
MIGRATIONS_NEEDED=$?

if [ $MIGRATIONS_NEEDED -eq 0 ]; then
    # Migrations needed, apply them
    python manage.py makemigrations
    python manage.py migrate
fi

# Check if superuser needs to be created
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists()" | grep "False" > /dev/null 2>&1
SUPERUSER_EXISTS=$?

if [ $SUPERUSER_EXISTS -eq 0 ]; then
    # Superuser does not exist, create it
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')" | python manage.py shell
fi

python manage.py runserver 0.0.0.0:8000
