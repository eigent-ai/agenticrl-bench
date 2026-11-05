from sqlalchemy import Column, Integer, String, Numeric, DateTime
from database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(255))
    sku = Column(String(50))
    price = Column(Numeric(10, 2))
    description = Column(String(1024))
    category = Column(String(100))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
