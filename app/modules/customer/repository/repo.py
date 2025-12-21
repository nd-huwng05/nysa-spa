from flask import g
from sqlalchemy import or_

from app.modules.customer.repository.models import Customer


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_customer_by_id(cus_id):
        return Customer.query.get(cus_id)

    @staticmethod
    def search_customer(data: str):
        filters = or_(Customer.fullname.like("%{}%".format(data.lower())),
                      Customer.phone.like("%{}%".format(data.lower())),
                      Customer.email.like("%{}%".format(data.lower())))
        customer = Customer.query.filter(filters).all()
        customer_list = [c.to_json() for c in customer]
        return customer_list

    def create_customer(self,code, data):
        new_customer = Customer(customer_code=code, fullname=data['fullname'], phone=data['phone'], address=data['address'], email=data['email'])
        self.db.session.add(new_customer)

    @staticmethod
    def search_customer_by_phone(data: str):
        return Customer.query.filter_by(phone=data).all()

    @staticmethod
    def search_customer_by_email(data: str):
        return Customer.query.filter_by(email=data).all()
