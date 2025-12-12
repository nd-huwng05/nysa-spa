from app.core.logger import logger
from app.core.errors import NewError
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

    def add_service_item(self, item_id:int, customer_id:int):
        try:
            self.repo.add_service_item(item_id, customer_id)
            self.repo.db.session.commit()
        except Exception as e:
            logger.error("Can't add service item {} to cart {}".format(item_id, e))
            raise NewError(status_code=500, message="INTERNAL_SERVER_ERROR")

    def remove_service_item(self, item_id:int):
        try:
            item = self.repo.get_cart_item_by_id(item_id)
            if item is None:
                raise NewError(status_code=404, message="SERVICE_NOT_FOUND_IN_CART")
            self.repo.remove_service_item(item)
            self.repo.db.session.commit()
        except Exception as e:
            logger.error("Can't remove service item {} to cart {}".format(item_id, e))
            raise NewError(status_code=500, message="INTERNAL_SERVER_ERROR")
