## imports
from marshmallow import Schema, fields

## cars_report schema
class CarsSchemaValidation(Schema):
    record_id = fields.String(required=True)
    today_date = fields.Date(format="%Y-%m-%d")
    category = fields.String(required=True)
    model = fields.String(required=True)
    make = fields.String(required=True)
    year = fields.Int(required=True)
