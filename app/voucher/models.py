import enum

from sqlalchemy import Column, String, Integer, Float, Enum, DateTime, Boolean, Table, ForeignKey
from app.interface.base_model import BaseModel


class TypeDiscound(enum.Enum):
    AMOUNT = 'amount'
    PERCENT = 'percent'

class Voucher(BaseModel):
    __tablename__ = 'voucher'

    name = Column(String(255),nullable=False)
    code = Column(String(255),nullable=False,unique=True)
    discount_type = Column(Enum(TypeDiscound), nullable=False,default=TypeDiscound.PERCENT)
    discount_value = Column(Float,nullable=False)
    start_date = Column(DateTime,nullable=False)
    end_date = Column(DateTime,nullable=False)
    description = Column(String(255), nullable=True)
    # min_order_amount = Column(Float,nullable=False)
    # max_order_amount = Column(Float,nullable=False)
    status = Column(Boolean,nullable=False,default=True)
