from datetime import datetime
from app import User, UserAuthMethod
from app import db

class Repository:
    @staticmethod
    def get_user_by_username(username: str) -> User:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        return User.query.get(user_id)

    @staticmethod
    def update_last_login_at(user_id: int):
        user_auth = UserAuthMethod.query.get(user_id)
        if user_auth:
            user_auth.last_login_at = datetime.now()
            db.session.commit()

