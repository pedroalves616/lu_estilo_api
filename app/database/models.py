from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


order_product_association = Table(
    'order_product_association', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', Integer, default=1)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="regular") 

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    orders = relationship("Order", back_populates="client")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    sale_price = Column(Float)
    barcode = Column(String, unique=True, index=True)
    section = Column(String, index=True)
    initial_stock = Column(Integer)
    current_stock = Column(Integer)
    expiration_date = Column(DateTime, nullable=True)
    images = Column(String, nullable=True) 

    orders = relationship("Order", secondary=order_product_association, back_populates="products")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    order_date = Column(DateTime, default=func.now())
    status = Column(String, default="pending") 
    total_amount = Column(Float)

    client = relationship("Client", back_populates="orders")
    products = relationship("Product", secondary=order_product_association, back_populates="orders")