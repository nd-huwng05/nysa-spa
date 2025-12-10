from flask import Blueprint
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    customer_routes = Blueprint('customer', __name__, template_folder='../templates', static_folder='../static', url_prefix='/customer')


    customer_routes.add_url_rule('/', view_func=c.index, methods=['GET'])

    app.register_blueprint(customer_routes)