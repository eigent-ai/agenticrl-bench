from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('sqlite:////app/data/products.db', echo=True)


class Base(DeclarativeBase):
    pass

Session = sessionmaker(bind=engine)
