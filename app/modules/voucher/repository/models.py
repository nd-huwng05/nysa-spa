import enum

from sqlalchemy import Column, Integer, String, Enum, DECIMAL, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import BaseModel


class DiscountType(enum.Enum):
    PERCENT = 'percent'
    FIXED = 'fixed'

class VoucherScope(enum.Enum):
    GLOBAL = 'global'
    SERVICE= 'service'
    HIDDEN = 'hidden'

class Voucher(BaseModel):
    __tablename__ = 'voucher'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    scope = Column(Enum(VoucherScope), server_default=VoucherScope.HIDDEN.value)
    owner_id = Column(Integer, ForeignKey('customer.id'))

    discount_type = Column(Enum(DiscountType), nullable=False)
    discount_value = Column(DECIMAL(12, 0), nullable=False)
    max_discount_amount = Column(DECIMAL(12, 0), nullable=True)
    min_order_value = Column(DECIMAL(12, 0), default=0)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    usage_limit = Column(Integer, server_default='0')
    usage_count = Column(Integer, server_default='0')
    limit_per_user = Column(Integer, server_default='1')
    active = Column(Boolean, server_default='1')

    owner = relationship("Customer", back_populates="vouchers")
    usages = relationship("VoucherUsage", back_populates="voucher")

class VoucherUsage(BaseModel):
    __tablename__ = 'voucher_usage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    voucher_id = Column(Integer, ForeignKey('voucher.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    invoice_id = Column(Integer, ForeignKey('invoice.id'), nullable=False)
    discount_amount = Column(DECIMAL(12, 0), nullable=False)

    voucher = relationship("Voucher", back_populates="usages")
    invoice = relationship("Invoice", back_populates="voucher_usage")