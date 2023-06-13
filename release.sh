#!/bin/bash
set -e
# python manage.py migrate
# python manage.py makesuperuser
python manage.py createsuperuser --username=admin --email=admin@example.com --password=123# --noinput

