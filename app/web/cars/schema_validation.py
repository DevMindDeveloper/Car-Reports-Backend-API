## imports
from datetime import date
from pydantic import BaseModel

## cars_report search schema
class CarsSchemaSearchValidation(BaseModel):
    today_date : date
    model : str
    make : str
    year : int

class SuccessModel(BaseModel):
    Items: list
