## imports
import subprocess as sp
import uvicorn

if __name__ == "__main__":
    sp.Popen("celery -A app.tasks.celery_app worker --loglevel=info", shell=True)
    sp.Popen("celery -A app.tasks.celery_app beat --loglevel=info", shell=True)
    uvicorn.run("app.app:app", host="127.0.0.1", port=1444, reload=True)
