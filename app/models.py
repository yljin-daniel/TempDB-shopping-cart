from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column('id', String(20), primary_key=True)
    name = Column('name', String(50), nullable=False)
    password = Column('password', String(20), nullable=False)
    address = Column('address', String(100))
    phone = Column('phone', String(20))
    birthday = Column('birthday', String(20))


class Goods(Base):
    __tablename__ = 'goods'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100), nullable=False)
    price = Column('price', Float)
    description = Column('description', String(200))
    brand = Column('brand', String(30))
    cpubrand = Column('cpu_brand', String(30))
    cputype = Column('cpu_type', String(30))
    memorycapacity = Column('memory_capacity', String(30))
    hdcapacity = Column('hd_capacity', String(30))
    cardmodel = Column('card_model', String(30))
    displaysize = Column('displaysize', String(30))
    image = Column('image', String(100))
    # One to many（Goods->OrderLineItem）
    orderLineItems = relationship('OrderLineItem')  


class Orders(Base):
    __tablename__ = 'orders'
    id = Column('id', String(20), primary_key=True)
    user_name = Column('user_name', String(20))
    orderdate = Column('order_date', String(20))
    status = Column('status', Integer)  
    total = Column('total', Float)
    # One to Many（Orders->OrderLineItem）
    orderLineItems = relationship('OrderLineItem')  


class OrderLineItem(Base):
    __tablename__ = 'orderLineItems'
    id = Column('id', Integer, primary_key=True)
    quantity = Column('quantity', Integer)
    subtotal = Column('sub_total', Float)
    goodsid = Column('goodsid', ForeignKey('goods.id'))  
    orderid = Column('orderid', ForeignKey('orders.id')) 
    # Many to one（OrderLineItem->Orders），reverse ref
    orders = relationship('Orders', backref='OrderLineItem') 
    # Many to ONe（OrderLineItem->Goods），reverse ref
    goods = relationship('Goods', backref='OrderLineItem') 
