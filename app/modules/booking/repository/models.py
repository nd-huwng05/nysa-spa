import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float, Text, DECIMAL
from sqlalchemy.orm import relationship, backref
from app.core.database import BaseModel


class BookingStatus(enum.Enum):
    PENDING = "PENDING"
    AWAITING_PAYMENT = "AWAITING PAYMENT"
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    NO_SHOW = "NO SHOW"

class Booking(BaseModel):
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_code = Column(String(20), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=True)
    booking_time = Column(DateTime, nullable=False)
    status = Column(Enum(BookingStatus), nullable=False, server_default=BookingStatus.PENDING.value)
    expires_at = Column(DateTime)
    total_amount = Column(DECIMAL(12,0), nullable=False, server_default='0.0')

    booking_details = relationship('BookingDetail', back_populates='booking')
    invoices = relationship("Invoice", back_populates="booking", cascade="all, delete-orphan")
    customer = relationship('Customer', back_populates='bookings')

class BookingDetail(BaseModel):
    __tablename__ = 'booking_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=True)
    duration_minutes = Column(Integer, default=60)
    price = Column(DECIMAL(12,0), server_default='0.0')
    parent_id = Column(Integer, ForeignKey('booking_detail.id'), nullable=True)
    notes = Column(Text, nullable=True)

    service = relationship('Service', back_populates='booking_details', uselist=False)
    booking = relationship("Booking", back_populates="booking_details")
    staff = relationship("Staff", back_populates="booking_details")
    children = relationship("BookingDetail", backref=backref('parent', remote_side=[id]),cascade="all, delete-orphan")