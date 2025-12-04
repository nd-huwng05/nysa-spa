from os import access

from flask_jwt_extended import create_access_token, create_refresh_token

from app.core.logger import logger
from ..config.config_module import ModuleConfig
from ..repository.models import User
from ..repository.repo import Repository

class Service:
    def __init__(self, repo: Repository, config: ModuleConfig):
        self.repo = repo
        self.config = config

    def auth_user_pass(self, username:str, password:str):
        user = self.repo.get_user_by_username(username)
        if not user or not user.check_password_hash(password):
            raise Exception('Invalid username or password')

        self.repo.update_last_login_at(user.id)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return access_token, refresh_token

    def google_callback(self, userinfo):
        user_id = None
        provider_id = userinfo.get('sub')
        user_auth_google = self.repo.get_user_auth_by_provider_id(provider_id)
        try:
            if not user_auth_google:
                avatar = userinfo.get('picture')
                name = userinfo.get('name')
                email = userinfo.get('email')
                user_has_email = self.repo.get_user_by_email(email)
                if not user_has_email:
                    user_id = self.repo.create_user(email, avatar, name)
                self.repo.create_auth_method(user_id, provider_id)
            else:
                user_id = user_auth_google.user_id
        except Exception as e:
            raise e

        access_token = create_access_token(identity=str(user_id))
        refresh_token = create_refresh_token(identity=str(user_id))
        return access_token, refresh_token

    def get_user_by_id(self, user_id: int) -> User:
        return self.repo.get_user_by_id(user_id)