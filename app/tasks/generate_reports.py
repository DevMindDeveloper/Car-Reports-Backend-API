import mysql.connector as mc
from celery import Celery
from marshmallow import ValidationError

from app import config as c
from app.tasks.schema_validation import carsSchemaValidation

## db_creds
db_configs = {
    'host' : c.host,
    'user' : c.user,
    'password' : c.password,
    'database' : c.database
}

## initialization
schema = carsSchemaValidation()

## celery app
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

## task
@celery_app.task
def save_data(recordID, today_date, category, model, make, year):

    ## db initialization
    conn = mc.connect(**db_configs)
    cursor = conn.cursor()

    try:
        car = schema.load({
            'recordID' : recordID,
            'today_date' : today_date,
            'category' : category,
            'model' : model,
            'make' : make,
            'year' : year
        })


        car_input = schema.dump(car)

        ## search existing records
        search_sql_query = "select recordID from cars_report where date = %s;"
        cursor.execute(search_sql_query, (car_input['recordID'],))
        res = cursor.fetchone()

        ## check records
        if res:
            return "Report already avaliable!"            

        ## store in DB
        insert_sql_query = "insert into cars_report (recordID, date, category, model, make, year) values (%s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_sql_query, (car_input['recordID'],
                                          car_input['today_date'],
                                          car_input['category'],
                                          car_input['model'],
                                          car_input['make'],
                                          car_input['year']))
        conn.commit()
    
    except mc.Error as er:
        print(f"Error: {er}")
    
    except ValidationError as err:
        print(f"Error: {err}")

    finally:
        ## close resources.
        cursor.close()
        conn.close()
        
    return "Report is generated!"   
