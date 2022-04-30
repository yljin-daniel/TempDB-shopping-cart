from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column('user_id', String(20), primary_key=True)
    name = Column('name', String(100))
    password = Column('password', String(100))
    email = Column('email', String(100))
    address = Column('address', String(100))
    phone = Column('phone_number', String(20))

class cart(Base):
    __tablename__='shopping_cart' # 表名
    id=Column('cart_id', Integer, primary_key=True)
    user_id=Column('user_id', String(64), unique=False)

class information(Base):
    __tablename__ = 'information'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(64), unique=False)
    lastName = Column(String(64), unique=False)
    payment = Column(String(64), unique=False)
    itemName = Column(String(64), primary_key=False)

