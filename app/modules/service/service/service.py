from ..config.config_module import ModuleConfig
from ..repository.repo import Repository

class Service:
    def __init__(self, repo, config):
        self.repo = repo
        self.config = config

    def get_filter_master_data(self):
        category = self.repo.get_all_category()
        badge = self.repo.get_all_badge()

        return {
            "category": category,
            "badge": badge,
        }

