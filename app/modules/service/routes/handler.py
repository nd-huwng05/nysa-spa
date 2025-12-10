from flask import Request, url_for

from app.extensions import oauth
from ..config.config_module import ModuleConfig
from ..service.service import Service


class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env


