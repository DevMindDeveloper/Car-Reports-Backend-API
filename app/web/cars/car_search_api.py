## imports
from fastapi import APIRouter, Depends

from app.models.cars.schema_car import Car
from app.tasks.schema_validation import CarInput
from app.web.auth import token_required
from app.web import session

## blueprint and prefix
search_cars_bp = APIRouter(prefix="/cars")

## car record search api
@search_cars_bp.post("/search_cars")
def search_cars(car_record : CarInput, id : int = Depends(token_required)):

    ## initialization
    car_dict = {
        "make": [],
        "model": [],
        "year": []
    }

    ## retrieving
    date = car_record.today_date
    make = car_record.make
    model = car_record.model
    year = car_record.year

    db_results = session.query(Car.make, Car.model, Car.year).filter(Car.date == date, Car.make == make,
                                                                    Car.model == model, Car.year == year).all()

    ## prepare dict for returning
    for db_res in db_results:
        car_dict['make'].append(db_res.make)
        car_dict['model'].append(db_res.model)
        car_dict['year'].append(db_res.year)

    return {"success":car_dict}, 200 # success
