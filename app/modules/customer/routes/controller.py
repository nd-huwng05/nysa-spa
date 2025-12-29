from flask import request, render_template, redirect, url_for, flash, session, Request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.extensions import oauth
from ..config.config_module import ModuleConfig
from ..service.service import Service
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    def index(self):
        return render_template('page/service.html')

    def update_info(self):
        try:
            self.handler.update_info(request)
            flash("UPDATE INFO SUCCESS", 'success')
            return "", 200
        except ValueError as e:
            flash(str(e))
            return "", 400
        except Exception as e:
            flash("INTERNAL SERVER ERROR", category="error")
            return "", 500

    def search(self):
        return self.handler.search(request)

    def create(self):
        return self.handler.create(request)

