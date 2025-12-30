from flask import request, render_template, redirect, url_for, flash, session, abort

from app.core.logger import logger
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    def index(self):
       return redirect(url_for('admin.dashboard'))

    def dashboard(self):
        try:
            data = self.handler.get_data_for_dashboard()
            return render_template('page/dashboard.html', **data)
        except Exception as e:
            logger.error("Error at admin index: {}".format(e))
            flash("INTERNAL SERVER ERROR", category="error")
            abort(500)

    def voucher(self):
        return render_template('page/voucher.html')

    def settings(self):
        try:
            data = self.handler.get_data_for_settings()
            print(data)
            return render_template('page/setting.html', **data)
        except Exception as e:
            logger.error("Error at admin settings: {}".format(e))
            flash("INTERNAL SERVER ERROR", category="error")
            abort(500)