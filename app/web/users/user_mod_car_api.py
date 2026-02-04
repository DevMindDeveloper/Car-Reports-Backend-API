## imports
from flask import request, jsonify
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from app.models.cars.schema_car import Car
from app.web.users.schema_validation import CarsSchemaModificationValidation
from app.web.auth import token_required
from app.web.cars import session, logger

## blueprint and prefix
user_mod_car_bp = Blueprint("cars_record_modification", __name__, url_prefix = "/cars")

@user_mod_car_bp.route("/<car_id>", methods=["PATCH"])
@user_mod_car_bp.arguments(CarsSchemaModificationValidation)
@user_mod_car_bp.response(200, CarsSchemaModificationValidation)
@token_required
def update_car(user_id, car_record, car_id):

    try:
        db_record = session.query(Car).filter(Car.record_id == car_id).first()
        if not db_record:
            logger.info("Record not avaliable!")
        
        ## update the record
        else:
            db_record.category = car_record.get('category', db_record.category)
            db_record.make = car_record.get('make', db_record.make)
            db_record.model = car_record.get('model', db_record.model)
            db_record.year = car_record.get('year', db_record.year)
            db_record.user_id = user_id

            session.commit()

            logger.info("Record updated!")
        
        return jsonify({"success":"record is up-to-date!"}), 200 # success
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error{e}")

@user_mod_car_bp.route("/<car_id>", methods=["DELETE"])
@token_required
def delete_car(id, car_id):

    try:    
        
        logger.info(f"deleting record {car_id}")
        delete_car_record = session.query(Car).filter(Car.record_id == car_id).first()
        if delete_car_record:

            session.delete(delete_car_record)
            session.commit()

            logger.info("Record is deleted from DB!")

            return jsonify({"success": "record is deleted!"}), 200 # success
        else:
            logger.info("Record is not in DB!")

            return jsonify({"success": "record is not avaliable!"}), 200 # success
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error{e}")

@user_mod_car_bp.route("/<car_id>", methods=["PUT"])
@user_mod_car_bp.arguments(CarsSchemaModificationValidation)
@user_mod_car_bp.response(200, CarsSchemaModificationValidation)
@token_required
def add_car(user_id, car_record, car_id):
    try:
        ## search already exsit records
        db_records = session.query(Car).filter(Car.record_id == car_id).first()
        if db_records:
            logger.info("Record already avaliable!")
        
        ## store in DB
        else:
            insert_car_record = Car(record_id = car_id, date = car_record['today_date'], category = car_record['category'],
                                    model = car_record['model'], make = car_record['make'], year = car_record['year'], user_id = user_id)
            
            session.add(insert_car_record)
            session.commit()

            logger.info("Record added!")
        
        return jsonify({"success":"record is added!"}), 200 # success
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error{e}")
