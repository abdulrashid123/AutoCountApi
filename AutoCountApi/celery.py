from __future__ import absolute_import,unicode_literals
import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoCountApi.settings')
app = Celery('AutoCountApi',broker='redis://127.0.0.1:6379')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')