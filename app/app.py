## imports
import subprocess as sp

from app import app
from app.web.cars.car_search_api import search_cars_bp
from app.web.users.user_account_api import users_pb

## register blueprints
app.register_blueprint(users_pb)
app.register_blueprint(search_cars_bp)

if __name__ == "__main__":
    sp.Popen("celery -A app.tasks.celery_app worker --loglevel=info", shell=True)
    sp.Popen("celery -A app.tasks.celery_app beat --loglevel=info", shell=True)
    app.run(host="127.0.0.1", port=1432)
