from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
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
    EMAIL = "email"
    LOCAL = "local"

class User(BaseModel):
    __tablename__ = 'user'

    username = Column(String(150), unique=True)
    password = Column(String(255))
    fullname = Column(String(50))
    avatar = Column(String(255), default="https://static.vecteezy.com/system/resources/thumbnails/027/951/137/small/stylish-spectacles-guy-3d-avatar-character-illustrations-png.png")
    phone = Column(String(150), unique=True)
    email = Column(String(150), unique=True)
    role = Column(Enum(RoleAccount), default=RoleAccount.CUSTOMER)

    auth_method = relationship("UserAuthMethod", backref="user", cascade="all, delete-orphan", lazy="selectin")
    staffs = relationship("Staff",backref="user" ,cascade="all, delete-orphan", lazy="selectin")

    def check_password_hash(self, password:str) -> bool:
        if hashlib.md5(password.encode()).hexdigest().__eq__(self.password):
            return True
        return False

    @property
    def is_admin(self) -> bool:
        return self.role == RoleAccount.ADMIN

    @property
    def is_staff(self) -> bool:
        return self.role == RoleAccount.STAFF

    @property
    def is_customer(self) -> bool:
        return self.role == RoleAccount.CUSTOMER

class UserAuthMethod(BaseModel):
    __tablename__ = 'user_auth_method'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    provider = Column(Enum(AuthMethodEnum), nullable=False)
    provider_id = Column(String(150), nullable=False)
    last_login_at = Column(DateTime, nullable=False)