from datetime import datetime
from decimal import Decimal
from enum import Enum
from app.extensions import db
from sqlalchemy import Column, DateTime, func


class BaseModel(db.Model):
    __abstract__ = True
    create_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    def to_dict(self):
        data = {}
        for column in self.__table__.columns:
            key = column.name
            value = getattr(self, key)

            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, Decimal):
                data[key] = str(value)
            elif isinstance(value, Enum):  # <--- Add this check
                data[key] = value.value
            elif key.startswith('_'):
                continue
            else:
                data[key] = value

        return data

    def to_json(self):
        return self.to_dict()