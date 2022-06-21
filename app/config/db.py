from dotenv import load_dotenv, find_dotenv

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

SQLALCHEMY_DATABASE_URL = 'mysql://{0}:{1}@{2}/{3}'.format(os.environ['MYSQL_LOGIN'], os.environ['MYSQL_PASSWORD'],
                                                           os.environ['MYSQL_HOST'], os.environ['MYSQL_DBNAME'])

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close_all()
