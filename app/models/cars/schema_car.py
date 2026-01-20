from sqlalchemy import Column, Integer, String
from app.models import *

## table structure
class Car(base):
    __tablename__ = "cars_report"

    id = Column(Integer, primary_key=True)
    recordID = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    make = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)

## creation
base.metadata.create_all(engine)
    