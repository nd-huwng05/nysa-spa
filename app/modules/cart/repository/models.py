from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import BaseModel

class CartItem(BaseModel):
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

    customer = relationship("Customer", back_populates="cart_items")
    service = relationship('Service', lazy='joined')