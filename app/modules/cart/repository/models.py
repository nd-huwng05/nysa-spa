from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import BaseModel


class Cart(BaseModel):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)

    items = relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")

class CartItem(BaseModel):
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

    service = relationship('Service', lazy='joined')