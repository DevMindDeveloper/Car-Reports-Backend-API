## imports
from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cars.schema_car import Car
from app.models.users.schema_user import User
from app.web.cars.schema_validation import CarsSchemaSearchValidation, SuccessModel
from app.web.auth import token_required
from app.web.cars import logger
from app.web.cars.utils import get_db

## blueprint and prefix
cars_reocrds_bp = APIRouter(prefix = "/cars")

## car record search api
@cars_reocrds_bp.get("/search_cars", response_model=SuccessModel, status_code = 200)
async def search_cars(car_record: CarsSchemaSearchValidation = Depends(), user_id : int = Depends(token_required), session: AsyncSession = Depends(get_db)):

    ## initialization
    car_dict = []

    try:
        ## retrieving
        db_result = await session.execute(select(User).where(user_id == user_id))
        db_user_record = db_result.scalar_one_or_none()

        ## prepare dict for returning
        for car in db_user_record.cars:
           if car.make == car_record.make and car.model == car_record.model and car.year == car_record.year:
               car_dict.append([car.make,car.model,car.year])

        return {"Items":car_dict}
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error: {e}")
