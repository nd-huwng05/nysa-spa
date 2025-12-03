import os
from . import settings
from flask import Config


class ModuleConfig:
    def __init__(self, global_config):
        self.global_config = global_config
        root_path = os.path.dirname(os.path.abspath(__file__))
        self.private_config = Config(root_path)
        self.private_config.from_object(settings)