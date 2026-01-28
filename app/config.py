class CarReportCredential():
    host = 'mysql'
    user = 'admin'
    password = '0126'
    database = 'user_cred_db'

    root_user = "root"
    root_password = "0126"

    app_secret_key = 'yourpassword'

        ## request parameter
    external_car_headers = {
        'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',
        'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'
    }

    external_car_url = 'https://parseapi.back4app.com/classes/Car_Model_List'

class RedisCred():
    broker = "redis://redis:6379/0"
    backend = "redis://redis:6379/0"
