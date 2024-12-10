from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DEV_DB_SERVER_URL = os.getenv("DEV_DB_SERVER_URL")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

except Exception as e:
    logging.exception(f"Error while connecting to database: {e}")
