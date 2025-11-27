from sys import deactivate_stack_trampoline

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import Relationship, relationship

from app.interface.base_model import BaseModel


class Service(BaseModel):
    __tablename__ = 'service'

    service_name = Column(String, primary_key=True,unique=True)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False, default=True)

    combo_id = Column(Integer, ForeignKey('combo.id'), nullable=False)
    service_combo = relationship('ServiceCombo', back_populates='service',lazy=True)

class ServiceCombo(BaseModel):
    __tablename__ = 'service_combo'

    service_id = Column(Integer, ForeignKey('service.id'), primary_key=True)
    combo_name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

