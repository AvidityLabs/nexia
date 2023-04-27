#!/bin/bash

# Delete all migration files except __init__.py
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Delete all compiled migration files (.pyc)
find . -path "*/migrations/*.pyc" -delete

python manage.py makemigrations
python manage.py migrate
