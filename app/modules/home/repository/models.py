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
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    url = Column(String(150))
    description = Column(Text)
    role = Column(Enum(RoleSection), server_default=RoleSection.DEFAULT.value)
