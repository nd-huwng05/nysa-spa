from flask import Request, url_for
from app.core.environment import Environment
from ..config.config_module import ModuleConfig
from ..service.service import Service


class Handler:
    def __init__(self, config: ModuleConfig, service: Service, env: Environment):
        self.config = config
        self.service = service
        self.env = env

    def login(self, request: Request):
        username = request.form.get('username')
        password = request.form.get('password')
        if not (username or password):
            raise Exception('Username and password are required')

        try:
            access_token, refresh_token = self.service.authenticate_local(username, password)
            return access_token, refresh_token
        except Exception as e:
            raise e

    def google_redirect(self):
        redirect_uri = url_for('user.google_auth', _external=True)
        return self.env.oauth.google.authorize_redirect(redirect_uri)

    def google_auth(self):
        token = self.env.oauth.google.authorize_access_token()
        user_info = self.env.oauth.google.parse_id_token(token, nonce=None)
        if not user_info:
            raise Exception('Invalid token google')

        access_token, refresh_token = self.service.authenticate_google(user_info)
        return access_token, refresh_token

    def get_information_user(self, user_id):
        return self.service.get_user_by_id(user_id)


