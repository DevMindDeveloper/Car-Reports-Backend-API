## imports
from sqlalchemy import Column, Integer, String

from app.models.base import Base

## table structure
class Car(Base):
    __tablename__ = "car_reports"

    make_key= "make"
    model_key= "model"
    year_key= "year"

    id = Column(Integer, primary_key=True)
    recordID = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    make = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)

    def to_json(self):
        return {
            self.make_key: self.make,
            self.model_key: self.model,
            self.year_key: self.year,
        }
