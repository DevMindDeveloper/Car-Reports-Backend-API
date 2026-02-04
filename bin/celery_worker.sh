#!/bin/sh

celery -A app.tasks.celery_app worker -Q reports --pool=prefork --concurrency=1 --loglevel=info
