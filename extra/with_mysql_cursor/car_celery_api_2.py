from celery.schedules import crontab
from datetime import timedelta

beat_schedule = {
    "daily-task" : {
        'task' : 'app.tasks.generate_reports.save_data',
        # 'schedule' : crontab(hour=2, minute=0)
        'schedule' : timedelta(hours=2),
    },
}
