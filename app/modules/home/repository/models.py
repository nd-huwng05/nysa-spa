import enum

from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import relationship

from app.core.database import BaseModel

class RoleSection(enum.Enum):
    DEFAULT = "default"
    CUSTOMER = "customer"
    STAFF = "staff"
    ADMIN = "admin"

class Section(BaseModel):
    __tablename__ = 'section'
    name = Column(String(150), nullable=False)
    description = Column(Text)
    role = Column(Enum(RoleSection), nullable=False, default=RoleSection.DEFAULT)
