from flask import Request, url_for

from app.extensions import oauth
from ..config.config_module import ModuleConfig
from ..service.service import Service


class Handler:
    def __init__(self, config, service, env):
        self.config = config
        self.service = service
        self.env = env

    def prepare_search_view_data(self):
        filter_options = self.service.get_filter_master_data()
        return {
            'filter': filter_options,
        }


