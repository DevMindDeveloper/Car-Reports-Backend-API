## imports
from app import app, engine
from app.web.cars.car_search_api import search_cars_bp
from app.web.users.user_account_api import users_pb
from app.models.base import Base

## register blueprints
app.register_blueprint(users_pb)
app.register_blueprint(search_cars_bp)

if __name__ == "__main__":
    Base.metadata.create_all(bind = engine)
    app.run(host="0.0.0.0", port=8080)
