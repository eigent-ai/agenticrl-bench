from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

CATEGORIES = ["Electronics", "Clothing", "Food", "Books", "Sports",
              "Toys", "Home", "Beauty", "Automotive", "Garden"]

engine = create_engine("sqlite:////app/products.db")
Base.metadata.create_all(engine)
with Session(engine) as s:
    for name in CATEGORIES:
        s.add(Category(name=name))
    s.commit()
print("Categories seeded.")
