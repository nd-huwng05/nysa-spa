from flask import request, render_template, redirect, url_for, flash, session
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.extensions import oauth
from ..config.config_module import ModuleConfig
from ..service.service import Service
from .handler import Handler

class Controller:
    def __init__(self, config:ModuleConfig, service:Service):
        self.handler = Handler(config, service)

    def login(self):
        if request.method == "GET":
            verify_jwt_in_request(optional=True)
            if get_jwt_identity() is None:
                return render_template('page/login.html')
            return redirect(url_for('home.public.index'))

        try:
            access_token, refresh_token = self.handler.login(request)
            response = redirect(url_for('home.public.index'))
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', refresh_token)
            return response

        except Exception as e:
            flash(str(e))
            return redirect(url_for('user.login'))

    def google_redirect(self):
        return self.handler.google_redirect()

    def google_auth(self):
        try:
            access_token, refresh_token = self.handler.google_auth()
            response = redirect(url_for('home.public.index'))
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', refresh_token)
            return response
        except Exception as e:
            flash(str(e))
            return redirect(url_for('user.login'))

    def logout(self):
        session.clear()
        response = redirect(url_for('home.public.index'))
        response.set_cookie('access_token', "")
        response.set_cookie('refresh_token', "")
        return response

    def load_logged_in_user(self):
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                user = self.handler.get_information_user(int(user_id))
                return {'current_user': user}
        except Exception:
            pass

        return {'current_user': None}


