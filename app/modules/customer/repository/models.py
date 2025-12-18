import enum
from sqlalchemy import Column, Integer, String, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import BaseModel

class MembershipTier(enum.Enum):
    STANDARD = 'STANDARD'
    SILVER = 'SILVER'
    GOLD = 'GOLD'
    PLATINUM = 'PLATINUM'

class Customer(BaseModel):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    customer_code = Column(String(10), unique=True, nullable=False)
    fullname = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    membership_tier = Column(Enum(MembershipTier), server_default=MembershipTier.STANDARD.value, nullable=False)
    points = Column(Integer, server_default='0')
    total_spent = Column(DECIMAL(12,0), server_default='0')

    user = relationship("User", back_populates="customer")
    bookings = relationship("Booking", back_populates="customer")
    cart_items = relationship("CartItem", back_populates="customer", cascade="all, delete-orphan")