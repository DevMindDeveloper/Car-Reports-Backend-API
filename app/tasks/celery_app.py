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
            "reports",
            queue_arguments={"x-max-priority" : 10},
        )
    }

    # beater for scheduling the task
    celery_app.conf.beat_schedule = {
        "daily-task" : {
            'task' : 'reports.save_data',
            'schedule' : timedelta(minutes=1),
            "options" : {"queue" : "reports", "priority" : 9}
        },
    }

    return celery_app

celery_app = create_celery_app()

## Custom logs output
class CustomLogger(Task):
    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"[SUCCESS] {self.name} returned {retval}")
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info(f"[SUCCESS] {self.name} returned {exc}")
