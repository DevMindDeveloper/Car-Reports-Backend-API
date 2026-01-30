import os

class CarReportCredential():
    host = os.getenv("MYSQL_HOST", default="mysql")
    database = os.getenv("MYSQL_DATABASE", default="db")

    root_user = os.getenv("MYSQL_ROOT_USER", default="root")
    root_password = os.getenv("MYSQL_ROOT_PASSWORD", default="1111")

    app_secret_key = os.getenv("APP_SECRET_KEY", default="1111")

        ## request parameter
    external_car_headers = {
        'X-Parse-Application-Id': os.getenv("EXTERNAL_CAR_HEADER_ID", default="car_111"),
        'X-Parse-Master-Key': os.getenv("EXTERNAL_CAR_HEADER_MASTER_KEY", default="1111")
    }

    external_car_url = 'https://parseapi.back4app.com/classes/Car_Model_List'

    database_url = f"mysql+pymysql://{root_user}:{root_password}@{host}:3306/{database}"

class RedisCred():
    broker = "redis://redis:6379/0"
    backend = "redis://redis:6379/0"
