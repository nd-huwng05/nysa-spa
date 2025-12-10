from flask import request,abort, render_template, redirect, url_for, flash, session, make_response, g
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from app.core.environment import Environment
from app.core.logger import logger
from ..config.config_module import ModuleConfig
from ..service.service import Service
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    @staticmethod
    def login():
        try:
            identity = getattr(g, 'current_user', None)
            if identity is None:
                return render_template('page/login.html')
            return redirect(url_for('home.index'))
        except Exception as e:
            logger.error("Can't render login page", data=e)
            abort(404)

    @staticmethod
    def logout():
        session.clear()
        response = make_response(redirect(url_for('home.index')))
        set_access_cookies(response, "")
        set_refresh_cookies(response, "")
        return response

    def auth_user_pass(self):
        try:
            access_token, refresh_token = self.handler.auth_user_pass(request)
            response = make_response(redirect(url_for('home.index')))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response

        except Exception as e:
            flash(str(e), category="error")
            return redirect(url_for('user.login'))

    def auth_google(self):
        return self.handler.auth_google()

    def google_callback(self):
        try:
            access_token, refresh_token = self.handler.google_callback()
            response = make_response(redirect(url_for('home.index')))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
        except Exception as e:
            flash(str(e), category="error")
            return redirect(url_for('user.login'))

    def middleware_load_user(self):
        self.handler.load_user()

    def push_data_to_template(self):
        return self.handler.push_data_to_template()



