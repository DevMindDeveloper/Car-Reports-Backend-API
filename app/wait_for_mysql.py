import time
import pymysql
from app.config import CarReportCredential
from app import logger

logger.info(f"Waiting for MySQL...")

while True:
    try:
        connection = pymysql.connect(
            host = CarReportCredential.host,
            user = CarReportCredential.root_user,
            password = CarReportCredential.root_password,
            port = 3306,
        )
        connection.close()
        logger.info("MySQL is ready!")
        break
    except pymysql.err.OperationalError:
        logger.info("MySQL is unavailable - sleeping 5s")
        time.sleep(5)
