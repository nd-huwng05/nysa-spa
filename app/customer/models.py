import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Table as SQLTable, Boolean, Date, Time
from sqlalchemy.orm import relationship
from app import db
from app.interface.base_model import BaseModel

class Customer(BaseModel):
    __tablename__ = 'customer'

    user_id = Column(Integer, ForeignKey('customer.id'), primary_key=True,nullable=False)
    fullname= Column(String(255),nullable=False)
    gender = Column(String(255),nullable=False)
    phone = Column(String(255),nullable=False)
    email = Column(String(255),nullable=False)
    address = Column(String(255),nullable=False)
    date_of_birth = Column(DateTime,nullable=False)