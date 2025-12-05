from flask import Blueprint
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config:ModuleConfig):
    c = Controller(service=service, config=config)

    service_routes = Blueprint('service', __name__, template_folder='../templates', static_folder='../static', url_prefix='/service')


    service_routes.add_url_rule('/service-view', view_func=c.service_view, methods=['GET'])

    app.register_blueprint(service_routes)