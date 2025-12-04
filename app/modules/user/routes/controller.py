from flask import request, render_template, redirect, url_for, flash, session, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, set_access_cookies, set_refresh_cookies

from app.core.environment import Environment
from ..config.config_module import ModuleConfig
from ..service.service import Service
from .handler import Handler

class Controller:
    def __init__(self, config:ModuleConfig, service:Service, env:Environment):
        self.handler = Handler(config, service, env)

    @staticmethod
    def login():
        verify_jwt_in_request(optional=True)
        if get_jwt_identity() is None:
            return render_template('page/login.html')
        return redirect(url_for('home.index'))

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
            flash(str(e))
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
            flash(str(e))
            return redirect(url_for('user.login'))



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


