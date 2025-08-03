# Use official Python 3.12 slim image
FROM python:3.12-slim

# Disable .pyc and buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install OS-level dependencies (for psycopg2 / PostgreSQL)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Prepare logs dir (for Django logging config)
RUN mkdir -p /app/logs && touch /app/logs/django.log

# Collect static files (WhiteNoise)
RUN python manage.py collectstatic --noinput

# Expose app port
EXPOSE 8000

# Start server with Gunicorn
CMD ["gunicorn", "Dudo_dent.wsgi:application", "--bind", "0.0.0.0:8000"]
