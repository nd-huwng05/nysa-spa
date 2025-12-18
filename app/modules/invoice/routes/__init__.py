from flask import Blueprint
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    invoice_routes = Blueprint('invoice', __name__, template_folder='../templates', static_folder='../static', url_prefix='/invoice')


    invoice_routes.add_url_rule('/payment', view_func=c.invoice_view, methods=['GET'])

    app.register_blueprint(invoice_routes)