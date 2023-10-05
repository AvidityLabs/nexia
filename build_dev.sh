pip install app/requirements/dev.txt
python3.9 manage.py collectstatic  --settings=core.settings.dev
python3.9 manage.py makemigrations --settings=core.settings.dev
python3.9 manage.py migrate --settings=core.settings.dev
python3.9 manage.py createsuperuser --username=admin --email=admin@example.com --noinput --settings=core.settings.dev