import time
import pymysql
from app.config import CarReportCredential

host = "mysql"  # Docker Compose service name
user = CarReportCredential.root_user
password = CarReportCredential.root_password

print(f"Waiting for MySQL at {host}...")

while True:
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=3306,
        )
        connection.close()
        print("MySQL is ready!")
        break
    except pymysql.err.OperationalError:
        print("MySQL is unavailable - sleeping 5s")
        time.sleep(5)
