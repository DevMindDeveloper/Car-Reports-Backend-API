## imports
from sqlalchemy import Column, Integer, String

from app.models.base import BASE

## table structure
class Car(BASE):
    __tablename__ = "car_reports"

    ID_KEY = "id"
    RECORDID_KEY = "recordID"
    DATE_KEY = "date"
    CATEGORY_KEY = "category"
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
            self.ID_KEY: self.id,
            self.RECORDID_KEY: self.recordID,
            self.DATE_KEY: self.date,
            self.CATEGORY_KEY: self.category,
            self.MODEL_KEY: self.model,
            self.MAKE_KEY: self.make,
            self.YEAR_KEY: self.year,
        }
