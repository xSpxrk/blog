import databases
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')

TESTING = os.getenv('TESTING')

if TESTING:
    POSTGRES_DB = os.getenv('POSTGRES_TEST_DB')
else:
    POSTGRES_DB = os.getenv('POSTGRES_DB')

DB_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}'

database = databases.Database(DB_URI)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DB_URI)

metadata.create_all(engine)
