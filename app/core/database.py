from app.extensions import db
from sqlalchemy import Column, Integer, DateTime, func

class BaseModel(db.Model):
    __abstract__ = True
    create_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())