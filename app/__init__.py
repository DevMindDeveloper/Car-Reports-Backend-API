from flask import Flask
from flask_bcrypt import Bcrypt
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import CarReportCredential

__all__ = ["engine", "session", "logger", "app", "bcrypt", "db", "migrate"]

## db_engine
engine = create_engine(CarReportCredential.DATABASE_URL)

## seesion for orm operation/sqlalchemy communications
Session = sessionmaker(bind=engine)
session = Session()

## logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

## initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = CarReportCredential.APP_SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = CarReportCredential.DATABASE_URL

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
