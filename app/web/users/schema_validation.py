## imports
from marshmallow import validate, Schema, fields

## users_cred schema
class UserSchemaValidation(Schema):
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8),
            validate.Regexp(
                r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).+$',
                error="Password must have upper, lower, digit & special char"
            )
        ]
    )

class CarsSchemaModificationValidation(Schema):
    today_date = fields.Date(format="%Y-%m-%d")
    category = fields.String(required=True)
    model = fields.String(required=True)
    make = fields.String(required=True)
    year = fields.Int(required=True)
