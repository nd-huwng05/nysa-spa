from click import option
from flask import Request, url_for, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.core.environment import Environment
from ..config.config_module import ModuleConfig
from ..service.service import Service


class Handler:
    def __init__(self, config: ModuleConfig, service: Service, env: Environment):
        self.config = config
        self.service = service
        self.env = env

    def auth_user_pass(self, request: Request):
        username = request.form.get('username')
        password = request.form.get('password')
        if not (username or password):
            raise Exception('Username and password are required')

        try:
            access_token, refresh_token = self.service.auth_user_pass(username, password)
            return access_token, refresh_token
        except Exception as e:
            raise e

    def auth_google(self):
        redirect_uri = url_for('user.google_callback', _external=True)
        return self.env.oauth.google.authorize_redirect(redirect_uri)

    def google_callback(self):
        token = self.env.oauth.google.authorize_access_token()
        user_info = self.env.oauth.google.parse_id_token(token, nonce=None)
        if not user_info:
            raise Exception('Invalid token google')

        access_token, refresh_token = self.service.google_callback(user_info)
        return access_token, refresh_token

    def get_information_user(self, user_id):
        return self.service.get_user_by_id(user_id)

    def load_user(self):
        g.current_user = None
        g.current_role = None
        try:
            verify_jwt_in_request(optional=True)
            identity = get_jwt_identity()
            if identity:
                g.current_user = self.service.get_user_by_id(identity)
                g.current_role = self.service.get_user_role_by_id(identity)

        except Exception:
            pass

    @staticmethod
    def push_data_to_template():
        user = getattr(g, 'current_user', None)
        role = getattr(g, 'current_role', None)
        return {
            'current_user': user,
            'current_role': role,
        }

