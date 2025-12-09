from flask import request, render_template, redirect, url_for, flash, session
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.core.environment import Environment
from app.extensions import oauth
from ..config.config_module import ModuleConfig
from ..service.service import Service
from .handler import Handler

class Controller:
    def __init__(self, config:ModuleConfig, service:Service, env: Environment):
        self.book_view = None
        self.handler = Handler(env, config, service)

    @staticmethod
    def book_view(self):
        return render_template('page/book_view.html')

    @staticmethod
    def book_confirm(self):
        return render_template('page/book_confirm.html')