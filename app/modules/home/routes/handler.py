from flask import Request, url_for, g

from app.extensions import oauth
from ..config.config_module import ModuleConfig
from ..service.service import Service


class Handler:
    def __init__(self, config: ModuleConfig, service: Service):
        self.config = config
        self.service = service

    def push_section_nav(self):
        role_auth_method = g.get('current_role', None)
        menu_nav = self.service.push_section_nav(role_auth_method)
        return {
            'menu_nav': menu_nav,
        }

