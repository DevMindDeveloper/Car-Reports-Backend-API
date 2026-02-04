## imports
from flask import request, jsonify
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from app.models.cars.schema_car import Car
from app.models.users.schema_user import User
from app.web.cars.schema_validation import CarsSchemaSearchValidation
from app.web.auth import token_required
from app.web.cars import session, logger

## blueprint and prefix
cars_reocrds_bp = Blueprint("cars", __name__, url_prefix = "/cars")

## car record search api
@cars_reocrds_bp.route("/search_cars", methods=["GET"])
@cars_reocrds_bp.arguments(CarsSchemaSearchValidation, location="query") #in-schema
@cars_reocrds_bp.response(200, CarsSchemaSearchValidation)  #out-schema
@token_required
def search_cars(user_id, car_record):

    ## initialization
    car_dict = []

    try:
        ## retrieving
        db_result = session.query(User).filter(user_id == user_id).first()
        cars = db_result.cars.filter(Car.make == car_record['make'], Car.model == car_record['model'], Car.year == car_record['year']).all()

        ## prepare dict for returning
        for car in cars:
           car_dict.append([car.make,car.model,car.year])

        return jsonify({"Items":car_dict}), 200 # success
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error: {e}")
