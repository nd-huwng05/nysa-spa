from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import BaseModel


class Cart(BaseModel):
    __tablename__ = 'cart'
    customer_id = Column(Integer, ForeignKey('customer.id'), unique=True, primary_key=True)

    customer = relationship("Customer", back_populates="cart")
    cart_items = relationship('CartItem', backref='cart_items', lazy=True, cascade="all, delete-orphan")

class CartItem(BaseModel):
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('cart.customer_id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

    cart = relationship('Cart', back_populates='cart_items')
    service = relationship('Service', lazy='joined')