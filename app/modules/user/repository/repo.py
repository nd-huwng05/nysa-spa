from datetime import datetime
from .models import User, UserAuthMethod, AuthMethodEnum, RoleAccount


class Repository:
    def __init__(self, env):
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
        return UserAuthMethod.query.filter_by(provider_id=provider_id).first()

    @staticmethod
    def update_last_login_at(user_id: int):
        UserAuthMethod.query.filter_by(user_id=user_id).update({'last_login_at': datetime.now()})

    def create_user(self, email: str, avatar: str, name: str) -> int:
        new_user = User(email=email, avatar=avatar, fullname=name, role=RoleAccount.CUSTOMER)
        self.db.session.add(new_user)
        self.db.session.flush()
        return new_user.id

    def create_auth_method_google(self, user_id: int, provider_id: int):
        new_auth_method = UserAuthMethod(user_id=user_id, provider_id=provider_id, provider=AuthMethodEnum.GOOGLE)
        self.db.session.add(new_auth_method)