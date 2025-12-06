from ..config.config_module import ModuleConfig
from ..repository.repo import Repository

class Service:
    def __init__(self, repo: Repository, config: ModuleConfig):
        self.repo = repo
        self.config = config

    def push_section_nav(self, role_auth_method):
        return self.repo.get_section_nav(role_auth_method)

