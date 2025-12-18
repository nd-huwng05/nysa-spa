from flask import g

from app.modules.customer.repository.models import Customer


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_customer_by_id(cus_id):
        return Customer.query.get(cus_id)