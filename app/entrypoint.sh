#!/bin/sh
set -e

echo "Running migrations..."
python3 manage.py makemigrations --noinput

# docker exec -it app python manage.py migrate --fake-initial # if you dont want to set it as main commands, can run it in container
# python3 manage.py migrate --fake-initial --noinput
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Creating superuser if it does not exist..."
python3 manage.py createsuperuser --username admin --email admin@localhost --noinput || true

echo "Starting Gunicorn..."
exec gunicorn -b 0.0.0.0:8000 ghanbari_store.wsgi:application
