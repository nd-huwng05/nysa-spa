from .routes.handler import Handler
from .repository.repo import Repository
from .config.config_module import ModuleConfig
from .routes.controller import Controller
from .service.service import Service
from .routes import register_routes
from app.core.environment import Environment


class VoucherModule:
    def __init__(self, app, env: Environment):
        self.app = app
        self.config = ModuleConfig(app.config)
        self.env = env
        repo = Repository(env)
        self.service = Service(repo=repo, config=self.config)

    def register(self):
        register_routes(self.app, self.service, self.config)

