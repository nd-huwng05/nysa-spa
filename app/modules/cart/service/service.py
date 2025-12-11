from ..config.config_module import ModuleConfig
from ..repository.repo import Repository

class Service:
    def __init__(self, repo:Repository, config):
        self.repo = repo
        self.config = config

    def push_count_service(self, customer_id:int):
        return self.repo.push_count_service(customer_id)

    def get_service_cart(self, customer_id:int):
        return self.repo.get_service_cart(customer_id)