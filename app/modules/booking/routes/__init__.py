from flask import Blueprint
from app.core.environment import Environment
from app.core.middleware import login_required, staff_required
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config:ModuleConfig, env:Environment):
    c = Controller(service=service, config=config, env=env)

    booking_routes = Blueprint('booking', __name__, template_folder='../templates', static_folder='../static', url_prefix='/booking')
    booking_routes.before_app_request(c.check_canceled_booking)


    booking_routes.add_url_rule('/appointment', view_func=login_required(c.book_view), methods=['GET'])
    booking_routes.add_url_rule('/appointment/staff', view_func=login_required(c.staff_appointment), methods=['GET'])
    booking_routes.add_url_rule('/create', view_func=login_required(c.booking_create), methods=['POST'])

    booking_routes.add_url_rule('/staff/list', view_func=login_required(staff_required(c.list_view_inner)), methods=['GET'])
    app.register_blueprint(booking_routes)