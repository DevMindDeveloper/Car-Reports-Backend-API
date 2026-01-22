from app import app
from app.web.users.user_account_api import users_pb
from app.web.cars.car_search_api import search_cars_bp

app.include_router(users_pb)
app.include_router(search_cars_bp)
