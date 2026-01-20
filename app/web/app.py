from app.web import *
import subprocess as sp

if __name__ == "__main__":
    sp.Popen("celery -A app.tasks.celery_worker worker --loglevel=info", shell=True)
    sp.Popen("celery -A app.tasks.celery_worker beat --loglevel=info", shell=True)
    app.run(host="127.0.0.1", port=1122)
    