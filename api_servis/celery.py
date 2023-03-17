import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CanalServisProject.settings')

app = Celery('api_servis')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'task_check_date_delivery_task': {
        'task': 'api_servis.tasks.check_date_delivery_task',
        'schedule': crontab(minute=15, hour=9),
    },
    'task_parse_google_sheets': {
        'task': 'api_servis.tasks.parse_google_sheets',
        'schedule': crontab(),
    },
}
