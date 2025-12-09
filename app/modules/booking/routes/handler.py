from ..config.config_module import ModuleConfig
from ..service.service import Service
from app.core.environment import Environment


class Handler:
    def __init__(self, env:Environment , config: ModuleConfig, service: Service):
        self.config = config
        self.service = service
        self.env = env



