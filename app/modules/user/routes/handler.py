from flask import Request, url_for, g, flash
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..service.service import Service


class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env

    def auth_user_pass(self, request: Request):
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return ValueError('Username and password are required')
        return self.service.auth_user_pass(username, password)


    def auth_google(self, request: Request):
        callback_url = request.args.get('callback_url')
        redirect_uri = url_for('user.google_callback', _external=True)
        return self.env.oauth.google.authorize_redirect(redirect_uri=redirect_uri, state=callback_url)

    def google_callback(self):
        token = self.env.oauth.google.authorize_access_token()
        user_info = self.env.oauth.google.parse_id_token(token, nonce=None)
        if not user_info:
            raise ValueError('Login failed')
        return self.service.google_callback(user_info)

    def user(self, id:int):
        user = self.service.get_user(id)
        if not user:
            return None
        return user
