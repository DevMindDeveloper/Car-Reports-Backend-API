## imports
from flask import request, jsonify
from flask_smorest import Blueprint

from app.models.cars.schema_car import Car
from app.web.cars.schema_validation import CarsSchemaSearchValidation
from app.web.auth import token_required
from app.web.cars import session, logger

## blueprint and prefix
search_cars_bp = Blueprint("search_cars", __name__, url_prefix = "/cars")

## car record search api
@search_cars_bp.route("/search_cars", methods=["GET"])
@search_cars_bp.arguments(CarsSchemaSearchValidation, location="query")
@token_required
def search_cars(id, car_record):

    ## initialization
    car_dict = []

    ## retrieving
    db_results = session.query(Car).filter(Car.date == car_record['today_date'], Car.make == car_record['make'],
                                           Car.model == car_record['model'], Car.year == car_record['year']).all()
    

    ## prepare dict for returning
    for db_res in db_results:
        car_record_display = db_res.to_json()
        car_dict.append([car_record_display['make'],car_record_display['model'],car_record_display["year"]])

    return jsonify({"success":car_dict}), 200 # success
