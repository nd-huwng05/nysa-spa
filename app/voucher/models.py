import enum

from sqlalchemy import Column, String, Integer, Float, Enum, DateTime, Boolean, Table as SQLTable, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from app.interface.base_model import BaseModel


class Typediscound(enum.Enum):
    AMOUNT = 'amount'
    PERCENT = 'percent'

Invoice_Voucher = SQLTable(
    'Invoice_Voucher',
    db.Model.metadata,
    Column('invoice_id', Integer, ForeignKey('invoice.id'),nullable=False),
    Column('voucher_id', Integer, ForeignKey('voucher.id'),nullable=False),
)

class Voucher(BaseModel):
    __tablename__ = 'voucher'

    name = Column(String(255),nullable=False)
    code = Column(String(255),nullable=False,unique=True)
    discount_type = Column(Enum(Typediscound), nullable=False,default=Typediscound.PERCENT)
    discount_value = Column(Float,nullable=False)
    start_date = Column(DateTime,nullable=False)
    end_date = Column(DateTime,nullable=False)
    min_order_amount = Column(Float,nullable=False)
    max_order_amount = Column(Float,nullable=False)
    status = Column(Boolean,nullable=False,default=True)

    invoice_voucher = relationship(
        'InvoiceVoucher',
        secondary=Invoice_Voucher,
        backref='invoice_voucher',
        lazy=True
    )
