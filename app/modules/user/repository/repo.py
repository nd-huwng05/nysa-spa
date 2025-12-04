from datetime import datetime

from app import logger
from app.core.environment import Environment
from .models import User, UserAuthMethod, AuthMethodEnum, RoleAccount


class Repository:
    def __init__(self, env: Environment):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_user_by_username(username: str):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email: str) -> User:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_auth_by_provider_id(provider_id):
        return UserAuthMethod.query.filter_by(provider_id=provider_id, provider=AuthMethodEnum.GOOGLE).first()

    def update_last_login_at(self, user_id: int):
        user_auth = UserAuthMethod.query.filter(user_id=user_id)
        for auth in user_auth:
            auth.last_login_at = datetime.now()
            self.db.session.commit()

    def create_user(self, email: str, avatar: str, name: str) -> int:
        try:
            new_user = User(email=email, avatar=avatar, fullname=name)
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user.id
        except Exception as e:
            logger.error("Don't create user {}".format(e))
            raise Exception("505 Server Error")

    def create_auth_method(self, user_id: int, provider_id: int):
        try:
            new_auth_method = UserAuthMethod(user_id=user_id, provider_id=provider_id, provider=AuthMethodEnum.GOOGLE, role=RoleAccount.CUSTOMER)
            self.db.session.add(new_auth_method)
            self.db.session.commit()
        except Exception as e:
            logger.error("Don't create auth method {}".format(e))
            raise Exception("505 Server Error")