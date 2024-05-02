from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import settings

db_url = 'postgresql://postgres:1@localhost:5432/order_db'

engine = create_engine(db_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()



def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

session = Session()
