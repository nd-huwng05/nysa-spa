import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, Text, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from app.core.database import BaseModel

class InvoiceType(enum.Enum):
    PAYMENT = 'PAYMENT'
    REFUND = 'REFUND'

class PaymentMethod(enum.Enum):
    CASH = 'CASH'
    BANK_TRANSFER = 'BANK_TRANSFER'

class PaymentType(enum.Enum):
    FULL = 'FULL'
    DEPOSIT = 'DEPOSIT'

class InvoiceStatus(enum.Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    FAILED = 'FAILED'

class Invoice(BaseModel):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_code = Column(String(50), unique=True, nullable=False)
    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    type = Column(Enum(InvoiceType), nullable=True, server_default=InvoiceType.PAYMENT.value)
    amount = Column(DECIMAL(12,0), nullable=True)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    payment_type = Column(Enum(PaymentType), nullable=True)
    status = Column(Enum(InvoiceStatus), server_default=InvoiceStatus.PENDING.value)
    note = Column(Text, nullable=True)
    expires_at = Column(DateTime)

    booking = relationship("Booking", back_populates="invoices")
