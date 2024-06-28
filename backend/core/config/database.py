from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import configparser


# Setup config
conf = configparser.ConfigParser()
conf.read('alembic.ini')

# Database connection
DB_URL = conf.get('alembic', 'sqlalchemy.url')
db_engine = create_engine(DB_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base()


def get_db() -> Session:  # type: ignore
    db = local_session()
    try:
        yield db
    finally:
        db.close()
