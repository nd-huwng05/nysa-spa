from flask import request, render_template, redirect, url_for, flash, session
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.extensions import oauth
from ..config.config_module import ModuleConfig
from ..service.service import Service
from .handler import Handler

class Controller:
    def __init__(self, config:ModuleConfig, service:Service):
        self.handler = Handler(config, service)

    def index(self):
        return render_template('page/service.html')


