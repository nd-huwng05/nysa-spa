from app import logger
from app.utils.pagination import Pagination
from ..config.config_module import ServiceConfig
from ..repository.repo import Repository

class Service:
    def __init__(self, repo: Repository, config: ServiceConfig):
        self.repo = repo
        self.config = config

    def get_filter_master_data(self):
        try:
            category = self.repo.get_all_category()
            badge = self.repo.get_all_badge()
            features = self.repo.get_all_features()
            return category, badge, features
        except Exception as e:
            logger.error("Can't get filter master data from repository", e)
            raise Exception("500 Internal Server Error")

    def get_list_services(self, pag: Pagination):
        try:
            services = self.repo.get_list_services(pag)
            total_items = self.repo.get_service_count()
            return services, pag.to_dict(total_items)
        except Exception as e:
            logger.error("Can't get list services from repository", e)

    def get_list_service_filter(self, filter, pag: Pagination):
        try:
            return self.repo.get_list_services_filter(filter, pag)
        except Exception as e:
            logger.error("Can't get list service filter from repository", e)
            raise Exception("500 Internal Server Error")



