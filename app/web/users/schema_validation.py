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
