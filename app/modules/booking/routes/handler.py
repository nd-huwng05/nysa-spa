from datetime import timedelta
from flask import g, Request
from app.utils.validation import validate_datetime
from ..config.config_module import BookingConfig
from ..service.service import Service

class Handler:
    def __init__(self, config:BookingConfig, service:Service, env):
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

    def handler_staff_appointment(self, request: Request):
        day = request.args.get('start')
        duration = request.args.get('duration', type=int)
        start = validate_datetime(day)
        end = start + timedelta(minutes=duration)
        staffs = self.env.modules.staff_module.service.get_staff_calendar(start, end)
        if not staffs:
            return {
            "staff_appointment": None
        }
        end = end + timedelta(minutes=self.config.private_config.get('TIME_REST'))
        staff_appointment = self.service.get_staff_appointment(staffs, start, end, self.config.private_config.get('LIMIT_APPOINTMENTS'))
        return {
            "staff_appointment": staff_appointment
        }


