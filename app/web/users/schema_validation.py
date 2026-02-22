## imports
import re
from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator

## users_cred schema
class UserSchemaValidation(BaseModel):
    email : EmailStr
    password : str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).+$'
        if not re.match(pattern, value):
            raise ValueError(
                "Password must have upper, lower, digit & special char"
            )
        return value

class SuccessModel(BaseModel):
    success: str

class FailureModel(BaseModel):
    error: str
    
class CarsSchemaModificationValidation(BaseModel):
    today_date : date
    category : str
    model : str
    make : str
    year : int
