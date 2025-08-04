import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dudo_dent.settings')

app = Celery('dudo_dent')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Manually set SSL config for Redis if using rediss://
if app.conf.broker_url and app.conf.broker_url.startswith("rediss://"):
    app.conf.broker_use_ssl = {'ssl_cert_reqs': 'CERT_NONE'}

if app.conf.result_backend and app.conf.result_backend.startswith("rediss://"):
    app.conf.redis_backend_use_ssl = {'ssl_cert_reqs': 'CERT_NONE'}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
