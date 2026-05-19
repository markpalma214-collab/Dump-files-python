from sqlalchemy import Column, String, Integer
from .database import Base

class Ecommerce(Base):
    __tablename__ = "ecommerce"
    id = Column(Integer, primary_key=True, index=True)
    users = Column(String)
    products = Column(String)
    orders = Column(String)
    order_items = Column(String)
    payments = Column(Integer)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
