import app.config as c
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

## db_engine
engine = create_engine(f"mysql+pymysql://{c.user}:{c.password}@{c.host}/{c.database}")  # mysql+pymysql://<user>:<password>@<host>/<database>
                    #    echo = True) 

base = declarative_base()

## seesion for orm operation/sqlalchemy communications
Session = sessionmaker(bind=engine)
session = Session()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
