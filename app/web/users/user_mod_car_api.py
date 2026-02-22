## imports
from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cars.schema_car import Car
from app.web.users.schema_validation import CarsSchemaModificationValidation, SuccessModel
from app.web.auth import token_required
from app.web.cars import logger
from app.web.users.utils import get_db

## blueprint and prefix
user_mod_car_bp = APIRouter(prefix = "/cars")

@user_mod_car_bp.patch("/{car_id}", response_model = SuccessModel, status_code = 200)
async def update_car(car_id: str, car_record: CarsSchemaModificationValidation, user_id: int = Depends(token_required), session: AsyncSession = Depends(get_db)):

    try:
        db_record = await session.execute(select(Car).where(Car.record_id == car_id))
        db_car_record = db_record.scalar_one_or_none()

        if not db_car_record:
            logger.info("Record not avaliable!")
        
        ## update the record
        else:
            db_car_record.category = car_record.category if car_record.category is not None else db_car_record.category
            db_car_record.make = car_record.make if car_record.make is not None else db_car_record.make
            db_car_record.model = car_record.model if car_record.model is not None else db_car_record.model
            db_car_record.year = car_record.year if car_record.year is not None else db_car_record.year
            db_car_record.user_id = user_id

            await session.commit()

            logger.info("Record updated!")
        
        return {"success":"record is up-to-date!"}
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error{e}")

@user_mod_car_bp.delete("/{car_id}")
async def delete_car(car_id: str, user_id: int = Depends(token_required), session: AsyncSession = Depends(get_db)):

    try:    
        
        logger.info(f"deleting record {car_id}")
        db_result = await session.execute(select(Car).where(Car.record_id == car_id))
        delete_car_record = db_result.scalar_one_or_none()

        if delete_car_record:

            await session.delete(delete_car_record)
            await session.commit()

            logger.info("Record is deleted from DB!")

            return {"success": "record is deleted!"}
        else:
            logger.info("Record is not in DB!")

            return {"success": "record is not avaliable!"}
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error{e}")

@user_mod_car_bp.put("/{car_id}", response_model=SuccessModel, status_code=200)
async def add_car(car_id: str, car_record: CarsSchemaModificationValidation, user_id: int = Depends(token_required), session: AsyncSession = Depends(get_db)):
    try:
        ## search already exsit records
        db_results = await session.execute(select(Car).where(Car.record_id == car_id))
        db_car_record = db_results.scalar_one_or_none()

        if db_car_record:
            logger.info("Record already avaliable!")
        
        ## store in DB
        else:
            insert_car_record = Car(record_id = car_id, date = car_record.today_date, category = car_record.category,
                                    model = car_record.model, make = car_record.make, year = car_record.year, user_id = user_id)
            
            session.add(insert_car_record)
            await session.commit()
            await session.refresh(insert_car_record)

            logger.info("Record added!")
        
        return {"success":"record is added!"}
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"DB error{e}")
