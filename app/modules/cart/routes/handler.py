from flask import g

from app.core.errors import NewError, NewPackage
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

    def add_service_item(self, item_id):
        if g.current_user.customer is None:
            raise NewError(403, "PERMISSION_DENIED")
        if item_id is None:
            raise NewError(400, "SERVICE IS REQUIRED")

        self.service.add_service_item(item_id, g.current_user.customer.id)
        return NewPackage(message="ADD SERVICE IS SUCCESSFULLY", status_code=201).response()

    def remove_service_item(self, item_id):
        if g.current_user.customer is None:
            raise NewError(403, "PERMISSION_DENIED")
        if item_id is None:
            raise NewError(400, "SERVICE IS REQUIRED")
        self.service.remove_service_item(item_id)
        return NewPackage(message="DELETE SERVICE IS SUCCESSFULLY", status_code=201).response()