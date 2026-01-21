from flask import Flask
from flask_bcrypt import Bcrypt
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import CarReportCredential

__all__ = ["engine", "session", "logger", "app", "bcrypt"]

## db_engine
""" mysql+pymysql://<user>:<password>@<host>/<database> """
engine = create_engine(f"mysql+pymysql://{CarReportCredential().user}:{CarReportCredential().password}@{CarReportCredential().host}/{CarReportCredential().database}")  
                    #    echo = True) 

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
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = CarReportCredential().app_secret_key
