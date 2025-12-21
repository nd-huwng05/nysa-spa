from flask import Blueprint
from app.core.environment import Environment
from app.core.middleware import jwt_middleware
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config:ModuleConfig, env:Environment):
    c = Controller(service=service, config=config, env=env)

    booking_routes = Blueprint('booking', __name__, template_folder='../templates', static_folder='../static', url_prefix='/booking')


    booking_routes.add_url_rule('/appointment', view_func=jwt_middleware(c.book_view), methods=['GET'])
    booking_routes.add_url_rule('/staff-appointment', view_func=jwt_middleware(c.staff_appointment), methods=['GET'])
    booking_routes.add_url_rule('/voucher', view_func=jwt_middleware(c.booking_voucher), methods=['GET'])
    booking_routes.add_url_rule('/create', view_func=jwt_middleware(c.add_booking), methods=['POST'])
    booking_routes.add_url_rule('/staff-book-view', view_func=c.staff_booking, methods=['GET'])
    booking_routes.add_url_rule('/staff-book-details', view_func=c.staff_booking_details, methods=['GET'])
    booking_routes.add_url_rule('/staff-appointment-json', view_func=c.staff_appointment_json, methods=['GET'])
    app.register_blueprint(booking_routes)