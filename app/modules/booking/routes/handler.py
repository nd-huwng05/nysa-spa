from flask import g, Request
from ..service.service import Service

class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env


    def handler_book_view(self, request: Request):
        service_ids = request.args.getlist('service')
        if not service_ids:
            return None, "You need choose least one service"

        services = self.env.modules.service_module.service.get_list_services_by_ids(service_ids)
        customer = None
        if g.current_user.role.value == "CUSTOMER":
            customer = g.current_user.customer

        return {
            "services": services,
            "customer": customer
        }, None



