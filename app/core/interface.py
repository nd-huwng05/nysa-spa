from abc import ABC, abstractmethod
from app.core.logger import logger


class ISettingObserver(ABC):
    @abstractmethod
    def update(self, setting_data: dict):
        raise NotImplementedError()

class IModule(ISettingObserver,ABC):
    def __init__(self, app, env, module_name: str):
        self.app = app
        self.env = env
        self.module_name = module_name
        self.config = None
        self.service = None
        self.repo = None


    def register(self, setting_module=None):
        if setting_module:
            setting_module.attach(self)

        self._register_routes()

    def update(self, setting_data: dict):
        data = setting_data.get(self.module_name, {})

        if data and self.config:
            self.config.reload(data)
            logger.info(f"[{self.module_name}] Settings updated from DB")

    @abstractmethod
    def _register_routes(self):
        pass
