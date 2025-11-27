import enum

from sqlalchemy import Column, ForeignKey, Integer, Table as SQLTable, DateTime, String, Boolean, Enum
from sqlalchemy.orm import relationship

from app import db
from app.interface.base_model import BaseModel

class StatusBooking(enum.Enum):
    BOOKED = 'booked'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    PENDING = 'pending'

BookingDetails = SQLTable(
    'BookingDetails',
    db.Model.metadata,
    Column('booking_id',Integer,ForeignKey('booking.id'),primary_key=True),
    Column('service_id',Integer,ForeignKey('service.id'),primary_key=True),
    Column('quantity',String(255),nullable=False)
)

ServiceSlip = SQLTable(
    'ServiceSlip',
    db.Model.metadata,
    Column('service_id',Integer,ForeignKey('service.id'),primary_key=True),
    Column('booking_id',Integer,ForeignKey('booking.id'),primary_key=True),
    Column('staff_id',Integer,ForeignKey('staff.id'),primary_key=True),
    Column('start_time',DateTime,nullable=False),
    Column('end_time',DateTime,nullable=False),
    Column('note',String(255),nullable=False)
)

class Booking(BaseModel):
    __tablename__ = 'booking'

    customer_id = Column(Integer,ForeignKey('customer.id'),primary_key=True)
    user_id = Column(Integer,ForeignKey('user.id'),primary_key=True)
    staff_id = Column(Integer,ForeignKey('staff.id'),primary_key=True)
    booking_date = Column(DateTime,nullable=False)
    booking_time = Column(DateTime,nullable=False)
    status = Column(Enum(StatusBooking),nullable=False,default=StatusBooking.PENDING)

    staff = relationship('Staff',back_populates='bookings',lazy=True,cascade='all ,delete-orphans')
    customer = relationship('Customer',back_populates='bookings',lazy=True,cascade='all ,delete-orphans')
    user = relationship('User',back_populates='bookings',lazy=True,cascade='all ,delete-orphans')
    invoices = relationship('Invoices',back_populates='bookings',lazy=True,cascade='all ,delete-orphans')

    services_booking = relationship(
        'Service',
        secondary=BookingDetails,
        back_populates='bookings',
        lazy = 'subquery',
    )

    service_slip = relationship(
        'ServiceSlip',
        secondary=ServiceSlip,
        back_populates='service_slip_bookings',
        lazy='subquery',
    )

