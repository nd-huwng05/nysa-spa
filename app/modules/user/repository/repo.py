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
    def get_user_auth_by_provider_id(provider_id):
        return UserAuthMethod.query.filter_by(provider_id=provider_id, provider=AuthMethodEnum.GOOGLE).first()

    def update_last_login_at(self, user_id: int):
        user_auth = UserAuthMethod.query.filter(user_id=user_id)
        for auth in user_auth:
            auth.last_login_at = datetime.now()
            self.db.session.commit()

    def create_user_with_google(self, email, avatar, fullname, provider_id):
        try:
            new_user = User(
                email=email,
                avatar=avatar,
                fullname=fullname,
                role=RoleAccount.CUSTOMER
            )
            self.db.session.add(new_user)
            self.db.session.flush()

            new_user_auth = UserAuthMethod(
                user_id=new_user.id,
                provider_id=provider_id,
                provider=AuthMethodEnum.GOOGLE,
                last_login_at=datetime.now(),
            )
            self.db.session.add(new_user_auth)
            self.db.session.commit()
            return new_user_auth

        except Exception as e:
            self.db.session.rollback()
            logger.error("Create user failed:", key=str(e))
            raise e