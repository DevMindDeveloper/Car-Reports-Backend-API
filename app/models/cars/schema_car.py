## imports
from app.models.cars import db

## table structure
class Car(db.Model):
    __tablename__ = "car_reports"

    ID_KEY = "id"
    RECORDID_KEY = "recordID"
    DATE_KEY = "date"
    CATEGORY_KEY = "category"
    MODEL_KEY= "model"
    MAKE_KEY= "make"
    YEAR_KEY= "year"

    id = db.Column(db.Integer, primary_key=True)
    recordID = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

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
