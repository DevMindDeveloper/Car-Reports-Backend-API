## imports
from flask import request, jsonify
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from app.models.cars.schema_car import Car
from app.web.cars.schema_validation import CarsSchemaSearchValidation
from app.web.auth import token_required
from app.web.cars import session, logger

## blueprint and prefix
cars_reocrds_bp = Blueprint("cars_records", __name__, url_prefix = "/cars")

## car record search api
@cars_reocrds_bp.route("/search_cars", methods=["GET"])
@cars_reocrds_bp.arguments(CarsSchemaSearchValidation, location="query")
@token_required
def search_cars(id, car_record):

    ## initialization
    car_dict = []

    try:
        ## retrieving
        db_results = session.query(Car).filter(Car.date == car_record['today_date'], Car.make == car_record['make'],
                                            Car.model == car_record['model'], Car.year == car_record['year']).all()
        

        ## prepare dict for returning
        for db_res in db_results:
            car_record_display = db_res.to_json()
            car_dict.append([car_record_display['make'],car_record_display['model'],car_record_display["year"]])

        return jsonify({"success":car_dict}), 200 # success
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error: {e}")

@cars_reocrds_bp.route("/patch_record", methods=["PATCH"])
def patch_record():
    car_record = request.get_json()

    try:
        ## search already exsit records
        db_records = session.query(Car).filter(Car.recordID == car_record['recordID']).first()
        if db_records:
            logger.info("Record already avaliable!")
        
        ## store in DB
        else:
            insert_car_record = Car(recordID = car_record['recordID'], date = car_record['today_date'], category = car_record['category'],
                                    model = car_record['model'], make = car_record['make'], year = car_record['year'])
            
            session.add(insert_car_record)
            session.commit()

            logger.info("Record added!")
        
        return jsonify({"success":"record is added!"}), 200 # success
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error{e}")

@cars_reocrds_bp.route("/delete_record", methods=["DELETE"])
def delete_record():
    received = request.get_json()

    try:    
        db_results = session.query(Car).all()
        received_records_ids = received['received_records_ids']

        for db_res in db_results:
            if db_res.recordID in received_records_ids:
                id_exist = True

            ## deletion
            elif not id_exist:
                logger.info("deleting record")
                delete_car_record = session.query(Car).filter(Car.recordID == db_res.recordID).first()            
                session.delete(delete_car_record)
                session.commit()

                logger.info("Record is deleted from DB!")
                continue

        return jsonify({"success": "records are deleted!"}), 200 # success
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error{e}")

@cars_reocrds_bp.route("/update_database", methods=["PUT"])
def update_database():
    received = request.get_json()

    try:
        db_results = session.query(Car).all()
        received_records = received['received_records']
        received_records_ids = received['received_records_ids']

        for db_res in db_results:
            if db_res.recordID in received_records_ids:
                for res in received_records:
                    if res.get("objectId") == db_res.recordID:
                        car_record = res
                        break

                ## updation
                db_res.category = car_record['Category']
                db_res.make = car_record['Make']
                db_res.model = car_record['Model']
                db_res.year = car_record['Year']

                logger.info("Record is up-to-date!")

        return jsonify({"success": "Record is up-to-date!"}), 200 # success
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error{e}")