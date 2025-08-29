FROM python:3.11-slim


# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SUPERUSER_PASSWORD=admin

# Create app directory
WORKDIR /app
COPY ./project /app

# Install dependencies
COPY ./requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc && \
    rm -rf /var/lib/apt/lists/*


# Run migrations & gunicorn at container start
CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1 ; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser --username admin --email admin@localhost --noinput || true ; \
    gunicorn -b 0.0.0.0:8000 ghanbari_store.wsgi:application




# # run Commands and Gunicorn
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "ghanbari_store.wsgi:application"]

