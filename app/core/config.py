import os
from flask import Config
from app.core.logger import logger


class ModuleConfig:
    def __init__(self, global_config, setting_module=None, root_path=None):
        self.global_config = global_config
        if root_path is None:
            root_path = os.getcwd()

        self.private_config = Config(root_path=root_path)
        if setting_module:
            self.private_config.from_object(setting_module)

    def reload(self, db_data: dict):
        if not db_data:
            return

        for key, value in db_data.items():
            self.private_config[key.upper()] = value

    def get(self, key, default=None):
        return getattr(self, key.upper(), default)

    def __getattr__(self, name):
        upper_name = name.upper()
        if upper_name in self.private_config:
            return self.private_config[upper_name]

        try:
            return getattr(self.global_config, name)
        except AttributeError:
            try:
                return getattr(self.global_config, upper_name)
            except AttributeError:
                pass
        logger.info(f'Setting Config {name} not found')
        raise AttributeError(f"Config '{name}' not found in Module or Global.")