from ..config.config_module import ModuleConfig
from ..repository.repo import Repository

class Service:
    def __init__(self, repo, config):
        self.repo = repo
        self.config = config
