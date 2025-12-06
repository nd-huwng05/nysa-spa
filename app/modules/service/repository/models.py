import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Boolean, DateTime, Table, Enum
from sqlalchemy.orm import relationship
from app.core.database import BaseModel

service_feature = Table(
    'service_feature',
    BaseModel.metadata,
    Column('service_id', Integer, ForeignKey('service.id'), primary_key=True),
    Column('feature_id', Integer, ForeignKey('feature.id'), primary_key=True)
)

service_combo = Table(
    'service_combo',
    BaseModel.metadata,
    Column('combo_id', Integer, ForeignKey('service.id'), primary_key=True),
    Column('service_id', Integer, ForeignKey('service.id'), primary_key=True)
)

class ServiceCategory(BaseModel):
    __tablename__ = 'service_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    services = relationship("Service", back_populates="category")

class Feature(BaseModel):
    __tablename__ = 'feature'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    icon = Column(String(50), nullable=False)

    services = relationship("Service", secondary=service_feature, back_populates="features")

class Badge(BaseModel):
    __tablename__ = 'badge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    color_code = Column(String(20))

    service_badges = relationship("ServiceBadge", back_populates="badge")

class ServiceType(enum.Enum):
    SINGLE = "single"
    COMBO = "combo"

class Service(BaseModel):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('service_category.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(12, 0), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    img_url = Column(String(255), nullable=False)
    is_active = Column(Boolean, server_default='1')
    type = Column(Enum(ServiceType), server_default=ServiceType.SINGLE.value)

    category = relationship("ServiceCategory", back_populates="services")
    features = relationship("Feature", secondary=service_feature, back_populates="services")
    service_badges = relationship("ServiceBadge", back_populates="service", cascade="all, delete-orphan")

    included_services = relationship(
        "Service",
        secondary=service_combo,
        primaryjoin=id == service_combo.c.combo_id,
        secondaryjoin=id == service_combo.c.service_id,
        backref="combos"
    )

class ServiceBadge(BaseModel):
    __tablename__ = 'service_badge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    badge_id = Column(Integer, ForeignKey('badge.id'), nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=True)

    service = relationship("Service", back_populates="service_badges")
    badge = relationship("Badge", back_populates="service_badges")