import enum

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from app.core.database import BaseModel

class Permission(BaseModel):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    staffs = relationship("StaffPermission", back_populates="permission")

class StaffPermission(BaseModel):
    __tablename__ = 'staff_permissions'
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False, primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False, primary_key=True)
    active = Column(Boolean, nullable=False, default=False)

    staff = relationship("Staff", back_populates="permissions")
    permission = relationship("Permission", back_populates="staffs")

class Staff(BaseModel):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_code = Column(String(10), unique=True, nullable=False)
    fullname = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    active = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="staff")
    calendars = relationship("StaffCalendar", back_populates="staff", cascade="all, delete-orphan")
    permissions = relationship("StaffPermission", back_populates="staff", cascade="all, delete-orphan")
    booking_details = relationship("BookingDetail", back_populates="staff", lazy='dynamic')


class StaffCalendar(BaseModel):
    __tablename__ = 'staff_calendar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    staff = relationship("Staff", back_populates="calendars")
