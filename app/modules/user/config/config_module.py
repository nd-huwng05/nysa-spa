import os
from app.core.config import ModuleConfig
from . import settings


class UserConfig(ModuleConfig):
    def __init__(self, global_config):
        root_path = os.path.dirname(os.path.abspath(__file__))

        super(UserConfig, self).__init__(
            global_config=global_config,
            setting_module=settings,
            root_path=root_path,
        )