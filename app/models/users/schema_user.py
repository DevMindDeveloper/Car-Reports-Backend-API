## imports
from sqlalchemy import Column, Integer, String

from app.models.base import BASE
from app.models.users import bcrypt

## table structure
class User(BASE):
    __tablename__ = "user_credentials"

    ID_KEY = "id"
    EMAIL_KEY = "email"

    id = Column(Integer, primary_key=True)
    email = Column(String(20), nullable=False)
    _password = Column(String(200), nullable=False)

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, val):
        self._password = bcrypt.generate_password_hash(val).decode("utf-8")
    
    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.EMAIL_KEY: self.email
        }
