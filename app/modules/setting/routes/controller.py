from flask import url_for, flash
from werkzeug.utils import redirect

from app.core.logger import logger
from .handler import Handler

class Controller:
    def __init__(self, service, env):
        self.handler = Handler( service, env)

    def update(self):
        try:
            self.handler.update()
            flash("Settings updated successfully", "success")
            return redirect(url_for('admin.setting'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('admin.setting'))
        except Exception as e:
            logger.error("An error occurred", data=e)
            flash("INTERNAL SERVER ERROR", "error")
            return redirect(url_for('admin.setting'))