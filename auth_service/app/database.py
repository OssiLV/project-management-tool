import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')  # auth_db

# Create DB if not exists
ROOT_DATABASE_URL = f"mysql+pymysql://root:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/"
root_engine = create_engine(ROOT_DATABASE_URL)
with root_engine.connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))

DATABASE_URL = f"mysql+pymysql://root:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()