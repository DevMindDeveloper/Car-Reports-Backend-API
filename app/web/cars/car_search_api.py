## imports
from flask import request, jsonify
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from app.models.cars.schema_car import Car
from app.web.cars.schema_validation import CarsSchemaSearchValidation
from app.web.auth import token_required

from app.web import session

## blueprint and prefix
search_cars_bp = Blueprint("search_cars", __name__, url_prefix = "/cars")

## car record search api
@search_cars_bp.route("/search_cars", methods=["POST"])
@search_cars_bp.arguments(CarsSchemaSearchValidation())
@token_required
def search_cars(id, car_record):

    ## initialization
    car_dict = {
        "make": [],
        "model": [],
        "year": []
    }

    ## retrieving
    date = car_record['today_date']
    make = car_record['make']
    model = car_record['model']
    year = car_record['year']

    db_results = session.query(Car.make, Car.model, Car.year).filter(Car.date == date, Car.make == make,
                                                                    Car.model == model, Car.year == year).all()

    ## prepare dict for returning
    for db_res in db_results:
        car_dict = Car.to_json(car_dict, db_res.make, db_res.model, db_res.year)

    return jsonify({"success":car_dict}), 200 # success
