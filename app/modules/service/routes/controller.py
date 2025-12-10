from flask import request, render_template, redirect, url_for, flash, session
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.extensions import oauth
from ..config.config_module import ModuleConfig
from ..service.service import Service
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    @staticmethod
    def service_search_view():
        return render_template('page/service_search.html')

    @staticmethod
    def service_detail_view():
        return render_template('page/service_detail.html')
