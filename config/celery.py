import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# app = Celery('hellotarot', backend='redis://', broker='redis://{rdis ip address}')
app = Celery("hellotarot")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


app.conf.beat_schedule = {
    "update-status-5-minutes": {
        "task": "check_game_status",
        "schedule": crontab(second="*/1")
    }
}