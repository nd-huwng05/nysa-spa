from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from app.interface.base_model import BaseModel
from sqlalchemy.orm import relationship, backref
import enum

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

    username = Column(String(150), nullable=True, unique=True)
    password = Column(String(150), nullable=True)
    fullname = Column(String(50), nullable=True)
    avatar = Column(String(150), default="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.iconpacks.net%2Ffree-icon%2Fuser-3296.html&psig=AOvVaw0MB6GuXKx0e4UcyX_oVPrw&ust=1763675778600000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLC4hLWa_5ADFQAAAAAdAAAAABAE")
    phone = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    role = Column(Enum(RoleAccount), default=RoleAccount.CUSTOMER)

    auth_method = relationship("UserAuthMethod", backref="user", cascade="all, delete-orphan", lazy="selectin")

class UserAuthMethod(BaseModel):
    __tablename__ = 'user_auth_method'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    provider = Column(Enum(AuthMethodEnum), nullable=False)
    provider_id = Column(String(150), nullable=False)
    last_login_at = Column(DateTime, nullable=False)