#!/bin/sh

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ "$DEBUG" = "true" ]; then
  echo "DEBUG MODE: Starting Celery worker manually later. Sleeping..."
  sleep infinity
elif [ "$RUN_WORKER" = "true" ]; then
  echo "Starting Celery worker..."
  exec celery -A Dudo_dent worker --loglevel=info
else
  echo "Starting Gunicorn server..."
  exec gunicorn Dudo_dent.wsgi:application --bind 0.0.0.0:8000
fi
