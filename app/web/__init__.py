from flask import Flask
from app import *

from app.models.cars.schema_car import Car
from app import config as c
from  flask_bcrypt import Bcrypt
from app.web.auth import token_required
from app.web.cars.utils import convert_date_to_desired_format
from app.tasks.schema_validation import CarsSchemaSearchValidation, UserSchemaValidation

## initialization
app = Flask(__name__)
bcrypt = Bcrypt(app)
schema = CarsSchemaSearchValidation()
schema_user = UserSchemaValidation()

app.config['SECRET_KEY'] = c.secret_key

from app.web.users import signup_api
from app.web.users import sigin_api
from app.web.users import profile_api
from app.web.cars import car_search_api
