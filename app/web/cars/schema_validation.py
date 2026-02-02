## imports
from marshmallow import Schema, fields

## cars_report search schema
class CarsSchemaSearchValidation(Schema):
    today_date = fields.Date(format="%Y-%m-%d")
    model = fields.String(required=True)
    make = fields.String(required=True)
    year = fields.Int(required=True)
