from datetime import datetime

from flask_jwt_extended import create_access_token, create_refresh_token

from app import RoleAccount, db
from app.user.models import User, UserAuthMethod, AuthMethodEnum
from app.user.repository import Repository

class Service:
    @staticmethod
    def get_by_name(name: str):
        pass

    @staticmethod
    def get_by_provider_id(provider_id: str):
        return UserAuthMethod.query.filter_by(provider_id=provider_id, provider=AuthMethodEnum.GOOGLE).first()

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
    def login_with_google(user_info):
        email = user_info.get('email')
        name = user_info.get('name')
        avatar = user_info.get('picture')
        provider_id = user_info.get('sub')
        user_auth_google = Service.get_by_provider_id(provider_id)
        if not user_auth_google:
            new_user = User(
                username=email,
                email=email,
                fullname=name,
                avatar=avatar,
                role=RoleAccount.CUSTOMER
            )
            db.session.add(new_user)
            db.session.flush()

            user_auth_google = UserAuthMethod(
                user_id=new_user.id,
                provider_id=provider_id,
                provider=AuthMethodEnum.GOOGLE,
                last_login_at=datetime.utcnow(),
            )
            db.session.add(user_auth_google)
            db.session.commit()

        access_token = create_access_token(identity=str(user_auth_google.user_id))
        refresh_token = create_refresh_token(identity=str(user_auth_google.user_id))
        Repository.update_last_login_at(user_auth_google.user_id)

        return {
            'user_id': user_auth_google.user_id,
            'access_token': access_token,
            'refresh_token': refresh_token
        }





    @staticmethod
    def get_information_user(user_id: int)->User:
        return Repository.get_user_by_id(user_id)