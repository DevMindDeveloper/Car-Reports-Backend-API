from fastapi import FastAPI
import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import CarReportCredential

__all__ = ["engine", "session", "logger", "app", "bcrypt", "db", "migrate"]

## db_engine
engine = create_engine(CarReportCredential.DATABASE_URL)

async_engine = create_async_engine(CarReportCredential.ASYNC_DATABASE_URL,
                             pool_pre_ping=True)

## seesion for orm operation/sqlalchemy communications
SessionLocal = sessionmaker(bind=engine)
AsyncSessionLocal = sessionmaker(bind=async_engine,
                       class_=AsyncSession,
                       expire_on_commit=False)

session = SessionLocal()

## logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

## initialization
app = FastAPI()
