## imports
from app import app, db
from app.web.cars.cars_records_api import cars_reocrds_bp
from app.web.users.user_account_api import users_pb

## register blueprints
app.register_blueprint(users_pb)
app.register_blueprint(cars_reocrds_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=8080)
