from celery import Celery
from celery.schedules import crontab
from django.utils import timezone
from config.celery import app

@app.task(name="check_game_status")
def check_game_status():
    pass