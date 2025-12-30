from .routes.handler import Handler
from .repository.repo import Repository
from .config.config_module import HomeConfig
from .routes.controller import Controller
from .service.service import Service
from .routes import register_routes
from app.core.environment import Environment
from app.modules.service import ServiceModule
from ...core.interface import IModule


class HomeModule(IModule):
    def __init__(self, app, env: Environment):
        super().__init__(app, env, module_name="home_module")
        self.config = HomeConfig(app.config)
        repo = Repository(env)
        self.service = Service(repo=repo, config=self.config)

        self.env.add_module(key="service_module",module=ServiceModule(self.app,self.env))

    def _register_routes(self):
        register_routes(self.app, self.service, self.config, self.env)
