#!/bin/sh
# /opt/venv/bin/python manage.py dumpdata --indent 4 > tareon.json

# /opt/venv/bin/python manage.py dumpdata --indent 4 --natural-foreign --natural-primary -e auth.permission -e contenttypes > tareon.json
# /opt/venv/bin/python manage.py migrate --run-syncdb

# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc"  -delete

# /opt/venv/bin/python manage.py remove_stale_contenttypes
# --- Run database migrations ---
echo "Applying Migrations..."
/opt/venv/bin/python manage.py makemigrations
/opt/venv/bin/python manage.py migrate
/opt/venv/bin/python manage.py showmigrations
# /opt/venv/bin/python manage.py flush
# /opt/venv/bin/python manage.py dbshell < sqlite_db_dump.sql

# /opt/venv/bin/python manage.py startapp faq
# /opt/venv/bin/python manage.py loaddata tareon.json
# --- Collect static files ---
echo "Collecting static files..."
/opt/venv/bin/python manage.py collectstatic --no-input
# /opt/venv/bin/python  manage.py test --no-input
echo "Creating Super User..."
/opt/venv/bin/python manage.py createsuperuser --no-input

# --- Start Gunicorn ---
echo "Starting Gunicorn..."
/opt/venv/bin/gunicorn tareon.wsgi:application --bind 0.0.0.0:8000




 