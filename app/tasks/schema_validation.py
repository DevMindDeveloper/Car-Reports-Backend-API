from marshmallow import validate, Schema, fields

## users_cred schema
class userSchemaValidation(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))

## cars_report schema
class carsSchemaValidation(Schema):
    recordID = fields.String(required=True)
    today_date = fields.Date(format="%Y-%m-%d")
    category = fields.String(required=True)
    model = fields.String(required=True)
    make = fields.String(required=True)
    year = fields.Int(required=True)