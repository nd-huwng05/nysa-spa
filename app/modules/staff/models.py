from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean, Date, Time
from app.core.database import BaseModel
from sqlalchemy.orm import relationship, backref
from app.extensions import db

class Permission(BaseModel):
    __tablename__ = 'permission'
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))


staff_permissions = db.Table(
    'staff_permissions',
    Column('staff_id', Integer, ForeignKey('staff.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True),
    Column('expiry',DateTime, nullable=True)
)

class Staff(BaseModel):
    __tablename__ = 'staff'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)
    fullname = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    status = Column(Boolean, default=True, nullable=False)

    calendars = relationship('StaffCalendar', backref='staff', lazy=True, cascade="all, delete-orphan")

    permissions = relationship(
        'Permission',
        secondary='staff_permissions',
        backref=backref('staff', lazy=True),
        lazy='subquery'
    )

class StaffCalendar(BaseModel):
    __tablename__ = 'staff_calendar'

    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False)
    work_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    accepted = Column(Boolean, nullable=False, default=False)
