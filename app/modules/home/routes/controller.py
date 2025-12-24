from flask import render_template, redirect, url_for, flash, abort
from flask_login import current_user
from app.core.logger import logger
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    @staticmethod
    def index():
        try:
            if current_user.is_authenticated and current_user.role.value == 'ADMIN':
                return redirect(url_for('admin.index'))
            elif current_user.is_authenticated and current_user.role.value  == 'STAFF':
                    return redirect(url_for('staff.index'))
            else:
                return render_template('page/index.html')
        except Exception as e:
            logger.error(e)
            flash("500 Internal Server Error", category="error")
            abort(500)