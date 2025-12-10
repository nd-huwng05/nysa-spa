from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean, Text, text, func
from app.core.database import BaseModel
from sqlalchemy.orm import relationship
import enum
import hashlib

class RoleAccount(enum.Enum):
    CUSTOMER = "customer"
    STAFF = "staff"
    ADMIN = "admin"

class AuthMethodEnum(enum.Enum):
    GOOGLE = "google"
    LOCAL = "local"

class User(BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True)
    password = Column(String(255))
    fullname = Column(String(255))
    avatar = Column(String(255), server_default="https://static.vecteezy.com/system/resources/thumbnails/027/951/137/small/stylish-spectacles-guy-3d-avatar-character-illustrations-png.png")
    email = Column(String(255), unique=True)

    auth_method = relationship("UserAuthMethod", backref="user", cascade="all, delete-orphan", lazy="selectin")

    def check_password_hash(self, password:str) -> bool:
        if hashlib.md5(password.encode()).hexdigest().__eq__(self.password):
            return True
        return False

class UserAuthMethod(BaseModel):
    __tablename__ = 'user_auth_method'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    provider = Column(Enum(AuthMethodEnum), nullable=False)
    provider_id = Column(Text, nullable=False)
    role = Column(Enum(RoleAccount), server_default=RoleAccount.CUSTOMER.value)
    last_login_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    active = Column(Boolean, server_default=text('1'))

    customer = relationship("Customer", back_populates="user_auth", uselist=False)
    staff = relationship("Staff", back_populates="user_auth", uselist=False)