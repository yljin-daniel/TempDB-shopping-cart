from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    name = Column('username', String(100), primary_key=True)
    password = Column('password', String(100))
    email = Column('email', String(50))
    address = Column('address', String(100))
    phone = Column('phone', String(20))

class cart(Base):
    __tablename__='cart' # 表名
    id=Column(Integer, primary_key=True)
    name=Column(String(64), unique=False)

class information(Base):
    __tablename__ = 'information'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(64), unique=False)
    lastName = Column(String(64), unique=False)
    payment = Column(String(64), unique=False)
    itemName = Column(String(64), primary_key=False)

