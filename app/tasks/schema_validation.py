## imports
from datetime import date
from marshmallow import validate, Schema, fields
from pydantic import BaseModel, EmailStr, constr

## users_cred schema
class UserSchemaValidation(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))

class UserInput(BaseModel):
    email : EmailStr
    password: constr(min_length=8) # type: ignore

## cars_report schema
class CarsSchemaValidation(Schema):
    recordID = fields.String(required=True)
    today_date = fields.Date(format="%Y-%m-%d")
    category = fields.String(required=True)
    model = fields.String(required=True)
    make = fields.String(required=True)
    year = fields.Int(required=True)

## cars_report search schema
class CarsSchemaSearchValidation(Schema):
    today_date = fields.Date(format="%Y-%m-%d")
    model = fields.String(required=True)
    make = fields.String(required=True)
    year = fields.Int(required=True)

class CarInput(BaseModel):
    today_date : date
    model : str
    make : str
    year : int
