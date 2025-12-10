import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, Text
from sqlalchemy.orm import relationship

from app.core.database import BaseModel

class InvoiceType(enum.Enum):
    PAYMENT = 'payment'
    REFUND = 'refund'

class PaymentMethod(enum.Enum):
    CASH = 'cash'
    BANK_TRANSFER = 'bank_transfer'

class InvoiceStatus(enum.Enum):
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'
    CANCELED = 'canceled'

class Invoice(BaseModel):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_code = Column(String(50), unique=True, nullable=False)
    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    type = Column(Enum(InvoiceType), nullable=False, server_default=InvoiceType.PAYMENT.value)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod),server_default=PaymentMethod.CASH.value ,nullable=False)
    status = Column(Enum(InvoiceStatus), server_default=InvoiceStatus.PENDING.value)
    note = Column(Text, nullable=True)

    booking = relationship("Booking", back_populates="invoices")
    voucher_usage = relationship("VoucherUsage", back_populates="invoice")
