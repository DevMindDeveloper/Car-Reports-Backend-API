## imports
from celery import Celery, Task
from celery.schedules import crontab
from datetime import timedelta
from kombu import Queue

from app.tasks import logger
from app.config import RedisCred

def create_celery_app():
    # celery app
    celery_app = Celery(
        "tasks",
        broker=RedisCred.broker,
        include="app.tasks.generate_reports",
        backend=RedisCred.backend,
    )

    # custom queue creation
    celery_app.conf.task_queues = {
        Queue(
            "reports"
        )
    }

    # beater for scheduling the task
    celery_app.conf.beat_schedule = {
        "daily-task" : {
            'task' : 'save_car_records',
            'schedule' : timedelta(minutes=1),
        },
    }

    return celery_app

celery_app = create_celery_app()
