## imports
import subprocess as sp

from app import app
from app.web.cars.car_search_api import search_cars_bp
from app.web.users.signup_api import sign_up_bp
from app.web.users.sigin_api import sign_in_bp
from app.web.users.profile_api import profile_bp

## register blueprints
app.register_blueprint(sign_up_bp)
app.register_blueprint(sign_in_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(search_cars_bp)

if __name__ == "__main__":
    sp.Popen("celery -A app.tasks.celery_app worker --loglevel=info", shell=True)
    sp.Popen("celery -A app.tasks.celery_app beat --loglevel=info", shell=True)
    app.run(host="127.0.0.1", port=1432)
