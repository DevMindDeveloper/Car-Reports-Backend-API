## imports
from sqlalchemy import Column, Integer, String

from app.models.base import Base
from app.models import engine

## table structure
class User(Base):
    __tablename__ = "users_cred"

    id = Column(Integer, primary_key=True)
    email = Column(String(20), nullable=False)
    password = Column(String(50), nullable=False)

## creation
Base.metadata.create_all(engine)
