## imports
from sqlalchemy import Column, Integer, String

from app.models.base import Base

## table structure
class Car(Base):
    __tablename__ = "car_reports"

    id = Column(Integer, primary_key=True)
    recordID = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    make = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)

    @staticmethod
    def to_json(car_dict, make, model, year):
        car_dict["make"].append(make)
        car_dict["model"].append(model)
        car_dict["year"].append(year)

        return car_dict
