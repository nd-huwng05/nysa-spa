from flask import g, session
from flask_login import current_user

from app.core.errors import NewError, NewPackage
from ..service.service import Service


class Handler:
    def __init__(self, config, service: Service, env):
        self.config = config
        self.service = service
        self.env = env

    def push_count_service(self):
        if not current_user.is_authenticated or not current_user.role.value == "CUSTOMER":
            return {'count': 0}
        return {
            'count_cart': self.service.push_count_service(current_user.customer.id),
        }

    def get_service_cart(self):
        if current_user.customer is None:
            return {}
        return self.service.get_service_cart(current_user.customer.id)

    def add_service_item(self, item_id):
        if current_user.customer is None:
            raise NewError(403, "PERMISSION_DENIED")
        if item_id is None:
            raise NewError(400, "SERVICE IS REQUIRED")

        self.service.add_service_item(item_id, current_user.customer.id)
        return NewPackage(message="ADD SERVICE IS SUCCESSFULLY", status_code=201).response()

    def remove_service_item(self, item_id):
        if current_user.customer is None:
            raise NewError(403, "PERMISSION_DENIED")
        if item_id is None:
            raise NewError(400, "SERVICE IS REQUIRED")
        self.service.remove_service_item(item_id)
        return NewPackage(message="DELETE SERVICE IS SUCCESSFULLY", status_code=201).response()

    @staticmethod
    def toggle_check(request):
        data = request.get_json()
        service_id = str(data.get('id'))
        is_checked = data.get('checked')
        checked_list = session.get('checked_in_cart', [])
        if is_checked:
            if service_id not in checked_list:
                checked_list.append(service_id)
        else:
            if service_id in checked_list:
                checked_list.remove(service_id)

        session['checked_in_cart'] = checked_list
        print('checked_in_cart', checked_list)
        session.modified = True

        return NewPackage(data=checked_list ,message="CHECK SERVICE IS SUCCESSFULLY", status_code=200).response()