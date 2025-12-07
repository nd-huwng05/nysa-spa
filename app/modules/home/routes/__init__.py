from flask import Blueprint
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config:ModuleConfig):
    c = Controller(service=service, config=config)

    home_routes = Blueprint('home', __name__, template_folder='../templates', static_folder='../static', static_url_path='/home/static', url_prefix='/')
    home_routes.app_context_processor(c.push_section_nav)

    home_routes.add_url_rule('/', view_func=c.index, methods=['GET'])

    app.register_blueprint(home_routes)