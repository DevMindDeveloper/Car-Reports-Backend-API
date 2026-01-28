## imports
import subprocess as sp

from app import app
from app.web.cars.car_search_api import search_cars_bp
from app.web.users.user_account_api import users_pb
from app.models.base import Base, engine

## register blueprints
app.register_blueprint(users_pb)
app.register_blueprint(search_cars_bp)

if __name__ == "__main__":
    sp.run("python3 -m app.wait_for_mysql", shell=True, check=True)
    sp.run("python3 -m app.sql_user_setup", shell=True, check=True)
    Base.metadata.create_all(bind = engine)
    app.run(host="0.0.0.0", port=1432)
