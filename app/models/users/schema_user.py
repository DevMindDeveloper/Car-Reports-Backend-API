## imports
from sqlalchemy import Column, Integer, String

from app.models.base import Base

## table structure
class User(Base):
    __tablename__ = "user_credentials"

    id = Column(Integer, primary_key=True)
    email = Column(String(20), nullable=False)
    password = Column(String(200), nullable=False)
