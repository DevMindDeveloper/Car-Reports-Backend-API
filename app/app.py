## imports
from app import app
from app.web.cars.cars_records_api import cars_reocrds_bp
from app.web.users.user_account_api import users_pb
from app.web.users.user_mod_car_api import user_mod_car_bp

## register blueprints
app.include_router(users_pb)
app.include_router(cars_reocrds_bp)
app.include_router(user_mod_car_bp)
