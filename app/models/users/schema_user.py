## imports
from sqlalchemy import Column, Integer, String

from app.models.base import Base
from app.models import bcrypt

## table structure
class User(Base):
    __tablename__ = "user_credentials"

    id = Column(Integer, primary_key=True)
    email = Column(String(20), nullable=False)
    password = Column(String(200), nullable=False)

    def encrypt_password(self, password):
        return bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self, hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)
