import uuid
from datetime import datetime
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

    def search_customer(self, data):
        return self.repo.search_customer(data)

    def search_customer_by_phone(self, data):
        return self.repo.search_customer_by_phone(data)

    def search_customer_by_email(self, data):
        return self.repo.search_customer_by_email(data)

    def get_customer_by_email(self, email):
        return self.repo.get_customer_by_email(email)

    def create_customer(self, data):
        customer_code = f"CUS{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:4].upper()}"
        self.repo.create_customer(customer_code, data)
        self.repo.db.session.commit()

    def create_customer_has_account(self, fullname, email, user_id):
        customer_code = f"CUS{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:4].upper()}"
        self.repo.create_customer_has_account(customer_code, fullname, email, user_id)
