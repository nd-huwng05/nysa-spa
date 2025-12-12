from app.core.errors import NewError
from .models import CartItem

class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def push_count_service(customer_id:int) -> int:
        return CartItem.query.filter_by(customer_id=customer_id).count()

    @staticmethod
    def get_service_cart(customer_id:int):
        return CartItem.query.filter_by(customer_id=customer_id).all()

    def add_service_item(self, item_id:int, customer_id:int):
        new_item = CartItem(customer_id=customer_id, service_id=item_id)
        self.db.session.add(new_item)

    @staticmethod
    def get_cart_item_by_id(id_item:int):
        return CartItem.query.get(id_item)


    def remove_service_item(self, items:CartItem):
        self.db.session.delete(items)