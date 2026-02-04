## imports
from app import app
from app.web.cars.cars_records_api import cars_reocrds_bp
from app.web.users.user_account_api import users_pb
from app.web.users.user_mod_car_api import user_mod_car_bp

## register blueprints
app.register_blueprint(users_pb)
app.register_blueprint(cars_reocrds_bp)
app.register_blueprint(user_mod_car_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
