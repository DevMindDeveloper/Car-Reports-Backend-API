from sqlalchemy import Column, Integer, String
from app.models import *

## table structure
class User(base):
    __tablename__ = "users_cred"

    id = Column(Integer, primary_key=True)
    email = Column(String(20), nullable=False)
    password = Column(String(50), nullable=False)

## creation
base.metadata.create_all(engine)
