## imports
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
import bcrypt

## table structure
class User(Base):
    __tablename__ = "users"

    ID_KEY = "id"
    EMAIL_KEY = "email"

    id = Column(Integer, primary_key=True)
    email = Column(String(20), nullable=False)
    _password = Column(String(200), nullable=False)

    cars = relationship("Car", foreign_keys="Car.user_id", back_populates="user", lazy = "selectin")

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, val):
        self._password = bcrypt.hashpw(val.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.EMAIL_KEY: self.email
        }
