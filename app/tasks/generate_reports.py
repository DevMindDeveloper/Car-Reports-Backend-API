from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update
from marshmallow import ValidationError
import requests
import datetime

from app.models.cars.schema_car import Car
from app.tasks import *

## task
@celery_app.task
def save_data():

    try:

        ## retreiving
        data = requests.get(url, headers=headers)
        results = data.json()['results']
        
        for res in results:
            today_date = datetime.date.today()
            recordID = res["objectId"]
            category = res["Category"]
            model = res["Model"]
            make = res["Make"]
            year = res["Year"]

            ## schema validation
            car = schema.load({
                'recordID' : recordID,
                'today_date' : today_date,
                'category' : category,
                'model' : model,
                'make' : make,
                'year' : year
            })

            car_input = schema.dump(car)

            ## search already exsit records
            res = session.query(Car).filter(Car.recordID == car_input['recordID']).first()
            if res:
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
        res_ids = [res['objectId'] for res in results]

        for res in db_results:
            if res.recordID in res_ids:
                id_exist = True

            ## deletion
            elif not id_exist:
                logger.info("deleting record")
                delete_car_record = session.query(Car).filter(Car.recordID == res.recordID).first()            
                session.delete(delete_car_record)
                session.commit()
                continue
            
            if id_exist:
                car_record = next((d for d in results if d.get("objectId") == res.recordID))
                ## updation
                if res.category != car_record['Category']:
                    logger.info("updating category")
                    stmt = (update(Car).where(Car.recordID == res.recordID).values(category = car_record['Category'], date = today_date))
                    session.execute(stmt)
                    session.commit()

                elif res.make != car_record['Make']:
                    logger.info("updating make")
                    stmt = (update(Car).where(Car.recordID == res.recordID).values(make = car_record['Make'], date = today_date))
                    session.execute(stmt)
                    session.commit()

                elif res.model != car_record['Model']:
                    logger.info("updating model")
                    stmt = (update(Car).where(Car.recordID == res.recordID).values(model = car_record['Model'], date = today_date))
                    session.execute(stmt)
                    session.commit()

                elif res.year != car_record['Year']:
                    logger.info("updating year")
                    stmt = (update(Car).where(Car.recordID == res.recordID).values(year = car_record['Year'], date = today_date))
                    session.execute(stmt)
                    session.commit()
                
                else:
                    logger.info("Report already up-to-date!")
                    continue
    
    except SQLAlchemyError as er:
        session.rollback()
        logger.error(f"Error: {er}")
    
    except ValidationError as err:
        logger.error(f"Error: {err}")

    finally:
        ## close resources.
        session.close()

    return "Report is generated!"   
