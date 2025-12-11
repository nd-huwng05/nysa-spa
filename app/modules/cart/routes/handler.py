from flask import g

from ..service.service import Service


class Handler:
    def __init__(self, config, service: Service, env):
        self.config = config
        self.service = service
        self.env = env

    def push_count_service(self):
        if g.current_user is None or g.current_user.customer is None:
            return {'count_cart': 0, }
        return {
            'count_cart': self.service.push_count_service(g.current_user.customer.id),
        }

    def get_service_cart(self):
        if g.current_user.customer is None:
            return {}
        return self.service.get_service_cart(g.current_user.customer.id)
