from flask_jwt_extended import create_access_token, create_refresh_token

from app import User
from app.user.repository import Repository

class Service:
    @staticmethod
    def get_by_name(name: str):
        pass

    @staticmethod
    def authenticate(username: str, password: str):
        user = Repository.get_user_by_username(username)

        user.check_password_hash(password)
        if not user or not user.check_password_hash(password):
            raise Exception("Username or password incorrect")

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        Repository.update_last_login_at(user.id)

        return {
            'user_id': user.id,
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @staticmethod
    def get_information_user(user_id: int)->User:
        return Repository.get_user_by_id(user_id)