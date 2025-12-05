from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from app.core.database import BaseModel

class Section(BaseModel):
    __tablename__ = 'section'
    name = Column(String(150), nullable=False)
    description = Column(Text)
    contents = relationship("SectionContent", back_populates="section", cascade="all, delete-orphan")

class SectionContent(BaseModel):
    __tablename__ = 'section_content'
    section_id = Column(Integer, nullable=False)
    key = Column(String(150), nullable=False)
    value = Column(Text)

class Event(BaseModel):
    __tablename__ = 'event'
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    details_url = Column(Text)


