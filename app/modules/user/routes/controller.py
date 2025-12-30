from flask import request, render_template, redirect, url_for, flash
from flask_login import logout_user, login_user, current_user
from ..service.service import Service
from .handler import Handler
from app.core.logger import logger

class Controller:
    def __init__(self, config, service:Service, env):
        self.handler = Handler(config, service, env)

    @staticmethod
    def login():
        callback_url = request.args.get('callback_url', '/')

        if current_user.is_authenticated:
            return redirect(callback_url)
        return render_template('page/login.html', callback_url=callback_url)

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('home.index'))

    def auth_user_pass(self):
        callback_url = request.form.get('callback_url', '/')
        try:
            user = self.handler.auth_user_pass(request)
            login_user(user)
            return redirect(callback_url)
        except ValueError as e:
            flash(str(e), category='error')
            return redirect(url_for('user.login', callback_url=callback_url))
        except Exception as e:
            logger.error(e)
            flash("Internal Server Error", category='error')
            return redirect(url_for('user.login',  callback_url=callback_url))


    def auth_google(self):
        return self.handler.auth_google(request)

    def google_callback(self):
        callback_url = request.args.get('state')
        try:
            user = self.handler.google_callback()
            login_user(user)
        except ValueError as e:
            flash(str(e), category='error')
        except Exception as e:
            logger.error(e)
            flash("Internal Server Error", category='error')
        finally:
            return redirect(url_for('user.login', callback_url=callback_url))

    def user(self, user_id):
        return self.handler.user(user_id)



