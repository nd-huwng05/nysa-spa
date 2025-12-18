from app.core.errors import NewError
from ..config.config_module import ModuleConfig
from ..repository.repo import Repository

class Service:
    def __init__(self, repo:Repository, config):
        self.repo = repo
        self.config = config

    def update_customer_info(self, data):
        cus_id = data.get("id")
        customer = self.repo.get_customer_by_id(cus_id)
        if not customer:
            raise ValueError("CUS_ID DOES NOT EXIST")

        if 'full_name' in data:
            customer.fullname = data['fullname']

        if 'phone' in data:
            customer.phone = data['phone']

        if 'address' in data:
            customer.address = data['address']

        return None