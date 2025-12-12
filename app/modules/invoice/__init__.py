from .routes.handler import Handler
from .repository.repo import Repository
from .config.config_module import InvoiceConfig
from .routes.controller import Controller
from .service.service import Service
from .routes import register_routes
from app.core.environment import Environment
from app.modules.voucher import VoucherModule
from app.modules.booking import BookingModule
from ...core.interface import IModule


class InvoiceModule(IModule):
    def __init__(self, app, env: Environment):
        super().__init__(app, env, module_name="home_module")
        self.config = InvoiceConfig(app.config)
        repo = Repository(env)
        self.service = Service(repo=repo, config=self.config)
        self.env.add_module('booking_module', BookingModule(self.app, env))
        self.env.add_module('voucher_module',VoucherModule(self.app, env))

    def _register_routes(self):
        register_routes(self.app, self.service, self.config, self.env)

