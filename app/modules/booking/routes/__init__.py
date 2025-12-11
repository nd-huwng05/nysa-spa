from flask import Blueprint
from app.core.environment import Environment
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config:ModuleConfig, env:Environment):
    c = Controller(service=service, config=config, env=env)

    booking_routes = Blueprint('book', __name__, template_folder='../templates', static_folder='../static', url_prefix='/book')


    booking_routes.add_url_rule('/book-view', view_func=c.book_view, methods=['GET'])
    # booking_routes.add_url_rule('/book-confirm', view_func=c.book_confirm(), methods=['GET'])

    app.register_blueprint(booking_routes)