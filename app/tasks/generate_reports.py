## imports
import datetime
import requests
from celery_singleton import Singleton
from marshmallow import ValidationError

from app.config import CarReportCredential
from app.tasks.schema_validation import CarsSchemaValidation
from app.tasks.celery_app import celery_app

from app.tasks import session, logger

## task
@celery_app.task(name="save_car_records", base = Singleton, queue = "reports")
def save_car_records():

    try:

        ## retreiving
        data = requests.get(url = CarReportCredential.external_car_url,
                            headers = CarReportCredential.external_car_headers)
        received_records = data.json()['results']
        received_records_ids = [record['objectId'] for record in received_records]
        
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

            ## store new records in DB
            requests.patch(url = CarReportCredential.patch_url, json=car_input)
        
        ## delete existing reocrds
        requests.delete(url = CarReportCredential.delete_url, json={'received_records': received_records,
                                                                    'received_records_ids': received_records_ids,
                                                                    })
        
        ## update the existing reocrds
        requests.put(url = CarReportCredential.put_url, json={'received_records': received_records,
                                                              'received_records_ids': received_records_ids,
                                                              })
    
    except ValidationError as err:
        logger.error(f"Error: {err}")

    return
