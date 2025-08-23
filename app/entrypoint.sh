#!/bin/sh
set -e

# echo "Waiting for database..."

# while ! python3 -c "import pymysql, os; pymysql.connect(host=os.environ['DB_HOST'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'], database=os.environ['DB_NAME'])" 2>/dev/null; do
#     echo "Database not ready yet..."
#     sleep 2
# done

# echo "Database is ready!"


echo "Running migrations..."
python3 manage.py makemigrations --noinput


# python manage.py migrate auth 0001 --fake
# python manage.py migrate

# docker exec -it app python manage.py migrate --fake-initial # if you dont want to set it as main commands can run it in container
python3 manage.py migrate --fake-initial --noinput
# python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Creating superuser if it does not exist..."
python3 manage.py createsuperuser --user admin --email admin@localhost --noinput || true

echo "Starting Gunicorn..."
exec gunicorn -b 0.0.0.0:8000 ghanbari_store.wsgi:application
