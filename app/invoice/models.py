import datetime
import enum

from sqlalchemy import Column, Float, Enum, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.interface.base_model import BaseModel

class StatusPayment(enum.Enum):
    SUCCESSED = "SUCCESSED"
    PENDING = "PENDING"
    FAILED = "FAILED"

class PaymentMethod(enum.Enum):
    CASH = 'cash'
    MOMO = 'momo'
    VNPAY = 'vnpay'

class Invoices(BaseModel):
    __tablename__ = 'invoices'

    amount = Column(Float , nullable=False)
    status_payment = Column(Enum(StatusPayment),nullable=False,default=StatusPayment.PENDING)

    payment= relationship('Payment',back_populates='invoices',lazy=True,cascade='all, delete-orphans')
    refund = relationship('Refund',back_populates='invoices',lazy=True,cascade='all, delete-orphans')

class Refunds(BaseModel):
    __tablename__ = 'refunds'

    invoices_id=Column(Integer,ForeignKey('invoices.id'),nullable=False)
    amount = Column(Float , nullable=False)
    reason = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False,default=True)
    created_at = Column(DateTime, nullable=False,default=datetime.utcnow)

class Payments(BaseModel):
    __tablename__ = 'payments'

    invoices_id = Column(Integer,ForeignKey('invoices.id'),nullable=False)
    payment_method = Column(Enum(PaymentMethod),nullable=False,default=PaymentMethod.MOMO)
    status = Column(Enum(StatusPayment),nullable=False,default=StatusPayment.SUCCESSED)
    code_bank = Column(String(255),nullable=False,unique=True)