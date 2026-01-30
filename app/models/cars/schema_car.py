## imports
from sqlalchemy import Column, Integer, String

from app.models.base import BASE

## table structure
class Car(BASE):
    __tablename__ = "car_reports"

    ID= "id"
    RECORDID= "recordID"
    DATE= "date"
    CATEGORY = "category"
    MODEL_KEY= "model"
    MAKE_KEY= "make"
    YEAR_KEY= "year"

    id = Column(Integer, primary_key=True)
    recordID = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    make = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)

    def to_json(self):
        return {
            self.ID: self.id,
            self.RECORDID: self.recordID,
            self.DATE: self.date,
            self.CATEGORY: self.category,
            self.MODEL_KEY: self.model,
            self.MAKE_KEY: self.make,
            self.YEAR_KEY: self.year,
        }
