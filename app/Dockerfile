# Base image
FROM python:3.11-alpine

# Environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV DJANGO_SUPERUSER_USERNAME=admin
# ENV DJANGO_SUPERUSER_EMAIL=admin@localhost
ENV DJANGO_SUPERUSER_PASSWORD admin

# Create app directory
RUN mkdir /app
WORKDIR /app

# Copy requirements
COPY ./requirements.txt .

# Install dependencies for mysqlclient and python packages
RUN apk update && apk add --no-cache gcc python3-dev musl-dev mariadb-dev \
    && pip install --upgrade pip \
    && pip install mysqlclient \
    && pip install -r requirements.txt \
    && apk del gcc python3-dev musl-dev


CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1 ; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --fake-initial --noinput && \
    # python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser --user admin --email admin@localhost --noinput || true ; \
    gunicorn -b 0.0.0.0:8000 ghanbari_store.wsgi:application


# # Copy entrypoint script
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# # Use entrypoint
# ENTRYPOINT ["/entrypoint.sh"]
