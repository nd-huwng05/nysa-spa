from flask import request, render_template, redirect, url_for, flash, session, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, set_access_cookies, set_refresh_cookies

from app.core.environment import Environment
from ..config.config_module import ModuleConfig
from ..service.service import Service
from .handler import Handler

class Controller:
    def __init__(self, config:ModuleConfig, service:Service, env:Environment):
        self.handler = Handler(config, service, env)

    def login(self):
        if request.method == "GET":
            verify_jwt_in_request(optional=True)
            if get_jwt_identity() is None:
                return render_template('page/login.html')
            return redirect(url_for('home.index'))

        try:
            access_token, refresh_token = self.handler.login(request)
            response = make_response(redirect(url_for('home.index')))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response

        except Exception as e:
            flash(str(e))
            return redirect(url_for('user.login'))

    def google_redirect(self):
        return self.handler.google_redirect()

    def google_auth(self):
        try:
            access_token, refresh_token = self.handler.google_auth()
            response = make_response(redirect(url_for('home.index')))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
        except Exception as e:
            flash(str(e))
            return redirect(url_for('user.login'))

    def logout(self):
        session.clear()
        response = make_response(redirect(url_for('home.index')))
        set_access_cookies(response, "")
        set_refresh_cookies(response, "")
        return response

    def load_logged_in_user(self):
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                user = self.handler.get_information_user(int(user_id))
                return {'current_user': user}
        except Exception as e:
            pass

        return {'current_user': None}


