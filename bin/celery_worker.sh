#!/bin/sh

celery -A app.tasks.celery_app worker -Q reports --pool=solo --loglevel=info
