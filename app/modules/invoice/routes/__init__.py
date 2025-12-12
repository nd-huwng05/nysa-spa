from flask import Blueprint

from app.core.middleware import jwt_middleware
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    invoice_routes = Blueprint('invoice', __name__, template_folder='../templates', static_folder='../static', url_prefix='/invoice')


    invoice_routes.add_url_rule('/invoice-view', view_func=jwt_middleware(c.invoice), methods=['GET'])

    app.register_blueprint(invoice_routes)