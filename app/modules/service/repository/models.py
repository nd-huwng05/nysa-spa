import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Boolean, DateTime, Table, Enum, JSON
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

service_category = Table(
    'service_category',
    BaseModel.metadata,
    Column('service_id', Integer, ForeignKey('service.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)


class Category(BaseModel):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    services = relationship("Service", secondary=service_category, back_populates="categories")


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
    name = Column(String(100), nullable=False)
    short_description = Column(Text)
    price = Column(DECIMAL(12, 0), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    img_url = Column(String(255), nullable=False)
    is_active = Column(Boolean, server_default='1')
    type = Column(Enum(ServiceType), server_default=ServiceType.SINGLE.value)

    categories = relationship("Category", secondary=service_category, back_populates="services")
    features = relationship("Feature", secondary=service_feature, back_populates="services")
    service_badges = relationship("ServiceBadge", back_populates="service", cascade="all, delete-orphan")
    details = relationship('ServiceDetail', back_populates='service', uselist=False, cascade="all, delete-orphan")
    included_services = relationship("Service", secondary=service_combo, primaryjoin=id == service_combo.c.combo_id,
                                     secondaryjoin=id == service_combo.c.service_id, back_populates="parent_combos")
    parent_combos = relationship("Service", secondary=service_combo, primaryjoin=id == service_combo.c.service_id,
                                 secondaryjoin=id == service_combo.c.combo_id, back_populates="included_services")


class ServiceBadge(BaseModel):
    __tablename__ = 'service_badge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    badge_id = Column(Integer, ForeignKey('badge.id'), nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=True)

    service = relationship("Service", back_populates="service_badges")
    badge = relationship("Badge", back_populates="service_badges")


class ServiceDetail(BaseModel):
    __tablename__ = 'service_detail'
    service_id = Column(Integer, ForeignKey('service.id'), primary_key=True)
    long_description = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    process_steps = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    contraindication = Column(Text, nullable=True)

    service = relationship("Service", back_populates="details")