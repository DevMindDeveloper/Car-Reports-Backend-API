from sqlalchemy import create_engine, text
from app.config import CarReportCredential

engine = create_engine(f"mysql+pymysql://{CarReportCredential.root_user}:{CarReportCredential.root_password}@mysql:3306")

with engine.connect() as connection:
    connection.execute(text(f"create database if not exists {CarReportCredential.database}"))
    connection.execute(text(f"CREATE USER IF NOT EXISTS '{CarReportCredential.user}'@'%' IDENTIFIED BY '{CarReportCredential.password}';"))
    connection.execute(text(f"grant all privileges on {CarReportCredential.database}.* to '{CarReportCredential.user}'@'%';"))
    connection.execute(text("flush privileges"))
