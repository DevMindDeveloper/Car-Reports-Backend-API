import requests
import datetime
import time
import mysql.connector as mc
from app import config as c
from app.tasks.generate_reports import save_data

## db_creds
db_configs = {
    'host' : c.host,
    'user' : c.user,
    'password' : c.password,
    'database' : c.database
}

## request parameter
headers = {
    'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',
    'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'
}

url = 'https://parseapi.back4app.com/classes/Car_Model_List?limit=10'

while True:

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

        ## save data in background
        res = save_data.delay(recordID, today_date, category, model, make, year)
        print(f"Task queued with ID: {res.id}")

##---------------------------------------------------------------------------------------------
        # ## db initialization
        # conn = mc.connect(**db_configs)
        # cursor = conn.cursor()

        # try:
        #     ## search existing records
        #     search_sql_query = "select recordID from cars_report where date = %s;"
        #     cursor.execute(search_sql_query, (recordID,))
        #     res = cursor.fetchone()

        #     ## check records
        #     if res:
        #         print("Reports already avaliable!")
        #         continue            

        #     ## store in DB
        #     insert_sql_query = "insert into cars_report (recordID, date, category, model, make, year) values (%s, %s, %s, %s, %s, %s);"
        #     cursor.execute(insert_sql_query, (recordID, today_date, category, model, make, year))
        #     conn.commit()

        # except mc.Error as er:
        #     print(f"Error: {er}")

        # finally:
        #     ## close resources.
        #     cursor.close()
        #     conn.close()
##---------------------------------------------------------------------------------------------

    ## wait for next day
    time.sleep(86400)
