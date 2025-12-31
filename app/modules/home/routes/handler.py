from flask import Request, url_for, g

from app.extensions import oauth
from app.utils.pagination import Pagination
from ..config.config_module import ModuleConfig
from ..service.service import Service


class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env

    def list_services(self):
        pag = Pagination(size=5,page=1)
        services , _ = self.env.modules.service_module.service.get_list_services(pag)
        pagination = Pagination(size=4,page=1)
        combo= self.env.modules.service_module.service.get_combo_services(pagination)
        print(combo)
        return{
            'services': services,
            'combo': combo
        }


