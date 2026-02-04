import os

class CarReportCredential():
    HOST = os.getenv("MYSQL_HOST", default="mysql")
    DATABASE = os.getenv("MYSQL_DATABASE", default="db")

    ROOT_USER = os.getenv("MYSQL_ROOT_USER", default="root")
    ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", default="1111")

    APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", default="1111")

        ## request parameter
    EXTERNAL_CAR_HEADERS = {
        'X-Parse-Application-Id': os.getenv("EXTERNAL_CAR_HEADER_ID", default="car_111"),
        'X-Parse-Master-Key': os.getenv("EXTERNAL_CAR_HEADER_MASTER_KEY", default="1111")
    }

    EXTERNAL_CAR_URL = 'https://parseapi.back4app.com/classes/Car_Model_List'

    DATABASE_URL = f"mysql+pymysql://{ROOT_USER}:{ROOT_PASSWORD}@{HOST}:3306/{DATABASE}"

    patch_url = "http://web:8080/cars/patch_record"
    delete_url = "http://web:8080/cars/delete_record"
    put_url = "http://web:8080/cars/update_database"

class RedisCred():
    BROKER = "redis://redis:6379/0"
    BACKEND = "redis://redis:6379/0"
