#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "MYSQL started"
fi

# python manage.py flush --no-input
# python manage.py migrate

exec "$@"