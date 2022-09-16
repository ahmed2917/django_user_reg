from argparse import Namespace
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drfknox.settings')
app = Celery('drfknox')
app.config_from_object('django.conf:settings', Namespace='CELERY')