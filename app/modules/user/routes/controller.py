from flask import request,abort, render_template, redirect, url_for, flash, session, make_response, g
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from ..service.service import Service
from .handler import Handler

class Controller:
    def __init__(self, config, service:Service, env):
        self.handler = Handler(config, service, env)

    @staticmethod
    def login():
        callback_url = request.args.get('callback_url', '/')
        identity = getattr(g, 'current_user', None)

        if g.current_role and g.current_role.value == "STAFF":
            print(g.current_role)
            return redirect('/staff/work-view')
        if identity:
            return redirect(callback_url)
        return render_template('page/login.html', callback_url=callback_url)

    @staticmethod
    def logout():
        callback_url = request.args.get('callback_url', '/')
        session.clear()
        response = make_response(redirect(callback_url))
        set_access_cookies(response, "")
        set_refresh_cookies(response, "")
        return response

    def auth_user_pass(self):
        callback_url = request.form.get('callback_url', '/')
        try:
            access_token, refresh_token = self.handler.auth_user_pass(request)
            response = make_response(redirect(url_for('user.login', callback_url=callback_url)))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response

        except Exception as e:
            flash(str(e), category="error")
            return redirect(url_for('user.login', callback_url=callback_url))

    def auth_google(self):
        return self.handler.auth_google(request)

    def google_callback(self):
        callback_url = request.args.get('state')
        try:
            access_token, refresh_token = self.handler.google_callback()
            response = make_response(redirect(url_for('user.login',callback_url=callback_url)))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
        except Exception as e:
            flash(str(e), category="error")
            return redirect(url_for('user.login', callback_url=callback_url))

    def middleware_load_user(self):
        self.handler.load_user()

    def push_data_to_template(self):
        return self.handler.push_data_to_template()



