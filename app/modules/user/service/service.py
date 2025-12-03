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

    def authenticate_local(self, username:str, password:str):
        user = self.repo.get_user_by_username(username)
        if not user or not user.check_password_hash(password):
            raise Exception('Invalid username or password')

        self.repo.update_last_login_at(user.id)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return access_token, refresh_token

    def authenticate_google(self, userinfo):
        provider_id = userinfo.get('sub')
        user_auth_google = self.repo.get_user_auth_by_provider_id(provider_id)
        if not user_auth_google:
            email = userinfo.get('email')
            name = userinfo.get('name')
            avatar = userinfo.get('picture')
            try:
                user_id = self.repo.create_user_with_google(email, avatar, name, provider_id)
            except Exception as e:
                raise Exception('Login by google failed')
        else:
            user_id = user_auth_google.user_id

        access_token = create_access_token(identity=str(user_id))
        refresh_token = create_refresh_token(identity=str(user_id))
        return access_token, refresh_token

    def get_user_by_id(self, user_id: int) -> User:
        return self.repo.get_user_by_id(user_id)