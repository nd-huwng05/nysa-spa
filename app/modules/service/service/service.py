import math

from flask_migrate import current
from sqlalchemy.testing.suite.test_reflection import metadata

from app.utils.pagination import Pagination
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

    def get_list_service(self, filter_data):
        return self.repo.get_services_by_filter(filter_data)

