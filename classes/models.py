from sqlalchemy import Column, Integer, ForeignKey, Float, String, Date, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)
    author = relationship('Publisher', backref='books')


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)
    shop = relationship('Shop', backref='stocks')
    book = relationship('Book', backref='stocks')


class Sale(Base):
    __tablename__ = 'sale'
    __table_args__ = (CheckConstraint('date_sale <= now()'),)
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)
    stock = relationship('Stock', backref='sales')





