from app.tasks.generate_reports import celery_app

if __name__ == "__main__":
    celery_app.worker_main()