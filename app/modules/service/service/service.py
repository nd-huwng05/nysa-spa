from ..config.config_module import ModuleConfig
from ..repository.repo import Repository

class Service:
    def __init__(self, repo: Repository, config: ModuleConfig):
        self.repo = repo
        self.config = config

    @staticmethod
    def get_list_info():
        print(1)
