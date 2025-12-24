from flask import Blueprint
from app.core.environment import Environment
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config:ModuleConfig, env:Environment):
    c = Controller(service=service, config=config, env=env)

    booking_routes = Blueprint('booking', __name__, template_folder='../templates', static_folder='../static', url_prefix='/booking')


    booking_routes.add_url_rule('/appointment', view_func=c.book_view, methods=['GET'])
    booking_routes.add_url_rule('/staff-appointment', view_func=c.staff_appointment, methods=['GET'])
    booking_routes.add_url_rule('/voucher', view_func=c.booking_voucher, methods=['GET'])
    booking_routes.add_url_rule('/create', view_func=c.add_booking, methods=['POST'])
    booking_routes.add_url_rule('/staff-book-view', view_func=c.staff_booking, methods=['GET'])
    booking_routes.add_url_rule('/staff-book-details', view_func=c.staff_booking_details, methods=['GET'])
    booking_routes.add_url_rule('/staff-appointment-json', view_func=c.staff_appointment_json, methods=['GET'])
    booking_routes.add_url_rule('/checkin', view_func=c.checkin, methods=['POST'])
    app.register_blueprint(booking_routes)