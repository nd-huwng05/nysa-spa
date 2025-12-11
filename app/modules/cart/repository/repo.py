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