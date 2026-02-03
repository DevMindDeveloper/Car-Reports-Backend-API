## imports
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

## table structure
class Car(Base):
    __tablename__ = "car_reports"

    ID_KEY = "id"
    RECORD_ID_KEY = "record_id"
    DATE_KEY = "date"
    CATEGORY_KEY = "category"
    MODEL_KEY= "model"
    MAKE_KEY= "make"
    YEAR_KEY= "year"

    id = Column(Integer, primary_key=True)
    record_id = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    make = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", foreign_keys = [user_id], back_populates = "cars")

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.RECORD_ID_KEY: self.record_id,
            self.DATE_KEY: self.date,
            self.CATEGORY_KEY: self.category,
            self.MODEL_KEY: self.model,
            self.MAKE_KEY: self.make,
            self.YEAR_KEY: self.year,
        }
