# celery_app.py
import os 
import time
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameshop.settings')

app = Celery('gameshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

@app.task
def debug_task():
    time.sleep(3)
    print('q')
