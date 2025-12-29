from flask import Blueprint
from app.core.environment import Environment
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config:ModuleConfig, env:Environment):
    c = Controller(service=service, config=config, env=env)

    booking_routes = Blueprint('booking', __name__, template_folder='../templates', static_folder='../static', url_prefix='/booking')


    booking_routes.add_url_rule('/appointment', view_func=c.book_view, methods=['GET'])
    booking_routes.add_url_rule('/appointment/staff', view_func=c.staff_appointment, methods=['GET'])
    booking_routes.add_url_rule('/create', view_func=c.booking_create, methods=['POST'])
    app.register_blueprint(booking_routes)