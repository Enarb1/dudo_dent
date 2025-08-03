#!/bin/sh

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Celery worker..."
celery -A Dudo_dent worker --loglevel=info &

echo "Starting Gunicorn server..."
exec gunicorn Dudo_dent.wsgi:application --bind 0.0.0.0:8000
