from flask import Blueprint
from app.core.environment import Environment
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    event_routes = Blueprint('event', __name__, template_folder='../templates', static_folder='../static', url_prefix='/event')


    event_routes.add_url_rule('/', view_func=c.index, methods=['GET'])

    app.register_blueprint(event_routes)