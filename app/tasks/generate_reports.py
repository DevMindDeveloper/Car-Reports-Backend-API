## imports
import datetime
from marshmallow import ValidationError
import requests
from sqlalchemy import update

from app.config import CarReportCredential
from app.models.cars.schema_car import Car
from app.tasks.schema_validation import CarsSchemaValidation
from app.tasks.celery_app import celery_app, CustomLogger
from app.tasks.utils import find_dict

from app.tasks import session, logger

## task
@celery_app.task(name="reports.save_data", base = CustomLogger)
def save_data():

    try:

        ## retreiving
        data = requests.get(url = CarReportCredential().external_car_url,
                            headers = CarReportCredential().external_car_headers)
        received_records = data.json()['results']
        
        for record in received_records:
            today_date = datetime.date.today()
            recordID = record["objectId"]
            category = record["Category"]
            model = record["Model"]
            make = record["Make"]
            year = record["Year"]

            ## schema validation
            car = CarsSchemaValidation().load({
                'recordID' : recordID,
                'today_date' : today_date,
                'category' : category,
                'model' : model,
                'make' : make,
                'year' : year
            })

            car_input = CarsSchemaValidation().dump(car)

            ## search already exsit records
            db_records = session.query(Car).filter(Car.recordID == car_input['recordID']).first()
            if db_records:
                logger.info("Record already avaliable!")
            
            ## store in DB
            else:
                insert_car_record = Car(recordID = car_input['recordID'], date = car_input['today_date'], category = car_input['category'],
                                        model = car_input['model'], make = car_input['make'], year = car_input['year'])
                
                session.add(insert_car_record)
                session.commit()

        ## update existing records
        id_exist = False
        db_results = session.query(Car).all()
        received_records_ids = [record['objectId'] for record in received_records]

        for db_res in db_results:
            if db_res.recordID in received_records_ids:
                id_exist = True

            ## deletion
            elif not id_exist:
                logger.info("deleting record")
                delete_car_record = session.query(Car).filter(Car.recordID == db_res.recordID).first()            
                session.delete(delete_car_record)
                session.commit()
                continue
            
            if id_exist:
                car_record = find_dict(received_records, "objectId", db_res.recordID)
                ## updation
                if db_res.category != car_record['Category']:
                    logger.info("updating category")
                    stmt = (update(Car).where(Car.recordID == db_res.recordID).values(category = car_record['Category'], date = today_date))
                    session.execute(stmt)
                    session.commit()

                elif db_res.make != car_record['Make']:
                    logger.info("updating make")
                    stmt = (update(Car).where(Car.recordID == db_res.recordID).values(make = car_record['Make'], date = today_date))
                    session.execute(stmt)
                    session.commit()

                elif db_res.model != car_record['Model']:
                    logger.info("updating model")
                    stmt = (update(Car).where(Car.recordID == db_res.recordID).values(model = car_record['Model'], date = today_date))
                    session.execute(stmt)
                    session.commit()

                elif db_res.year != car_record['Year']:
                    logger.info("updating year")
                    stmt = (update(Car).where(Car.recordID == db_res.recordID).values(year = car_record['Year'], date = today_date))
                    session.execute(stmt)
                    session.commit()
                
                else:
                    logger.info("Report already up-to-date!")
                    continue
    
    except ValidationError as err:
        logger.error(f"Error: {err}")

    return
