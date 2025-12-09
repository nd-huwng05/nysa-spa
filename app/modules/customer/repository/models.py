import enum
from sqlalchemy import Column, Integer, String, Enum, Float
from sqlalchemy.orm import relationship

from app.core.database import BaseModel

class MembershipTier(enum.Enum):
    STANDARD = 'standard'
    SILVER = 'silver'
    GOLD = 'gold'
    PLATINUM = 'platinum'

class Customer(BaseModel):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_code = Column(String(10), unique=True, nullable=False)
    fullname = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    membership_tier = Column(Enum(MembershipTier), server_default=MembershipTier.STANDARD.value, nullable=False)
    points = Column(Integer, server_default='0')
    total_spent = Column(Float, server_default='0')

    bookings = relationship("Booking", back_populates="customer")