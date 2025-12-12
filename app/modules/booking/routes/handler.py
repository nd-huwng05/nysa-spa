from flask import request, g

from ..service.service import Service

class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env


    def handler_book_view(self):
        service_id = request.args.get('services','')

        if not service_id:
            return None, "Vui lòng chọn ít nhất một dịch vụ hoặc một Combo."

        id_list_services = [int(s_id) for s_id in service_id.split(',') if s_id.isdigit()]

        services = self.env.modules.service_module.service.get_list_services(id_list_services)


        if g.current_user.customer is None:
            return None, "Bạn không có quyền customer"



        return {
            "services": services,
            "customer": g.current_user.customer
        }, None



