
from app import *
from celery import Celery
from app.tasks.schema_validation import CarsSchemaValidation

## initialization
schema = CarsSchemaValidation()

## celery app
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

## request parameter
headers = {
    'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',
    'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'
}

url = 'https://parseapi.back4app.com/classes/Car_Model_List'
