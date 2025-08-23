#!/bin/sh
# set -e

# echo "🚀 Starting container..."

# # Health check for mysqlclient
# python - <<EOF
# try:
#     import MySQLdb
#     print("✅ mysqlclient import OK")
# except Exception as e:
#     print("❌ mysqlclient import failed:", e)
#     exit(1)
# EOF

# Django setup
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
python3 manage.py createsuperuser --username admin --email admin@localhost --noinput || true

# Run gunicorn
exec gunicorn -b 0.0.0.0:8000 ghanbari_store.wsgi:application
