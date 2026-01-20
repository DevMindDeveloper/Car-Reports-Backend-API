from app.tasks import *
from celery.schedules import crontab
from datetime import timedelta

celery_app.autodiscover_tasks(["app.tasks"])

import app.tasks.generate_reports

celery_app.conf.beat_schedule = {
    "daily-task" : {
        'task' : 'app.tasks.generate_reports.save_data',
        # 'schedule' : crontab(hour=2, minute=0)
        'schedule' : timedelta(minutes=2),
    },
}
    