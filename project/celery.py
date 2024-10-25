from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    "update_info_for_tracks": {
        "task": "track_number.tasks.update_info_for_tracks",
        "schedule": crontab(minute='*')  # Запуск каждую минуту
    }
}

app.autodiscover_tasks()
