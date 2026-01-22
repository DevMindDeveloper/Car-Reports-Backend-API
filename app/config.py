class CarReportCredential():
    host = 'localhost'
    user = 'admin'
    password = '0126'
    database = 'user_cred_db'

    app_secret_key = 'yourpassword'

        ## request parameter
    external_car_headers = {
        'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',
        'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'
    }

    external_car_url = 'https://parseapi.back4app.com/classes/Car_Model_List'

class RedisCred():
    broker = "redis://localhost:6379/0"
    backend = "redis://localhost:6379/0"
