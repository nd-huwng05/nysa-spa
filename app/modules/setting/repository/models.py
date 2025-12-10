import enum

from sqlalchemy import Column, Integer, String, Text

from app.core.database import BaseModel

class SettingType(enum.Enum):
    Text = "text"
    INT = "int"
    Float = "float"
    BOOLEAN = "boolean"
    JSON = "json"
    DATETIME = "datetime"
    IMAGE = "image"

class Setting(BaseModel):
    __tablename__ = 'setting'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(50), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    type = Column(String(50), server_default='global', nullable=False)
