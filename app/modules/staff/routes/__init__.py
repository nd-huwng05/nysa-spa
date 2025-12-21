from flask import Blueprint
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    staff_routes = Blueprint('staff', __name__, template_folder='../templates', static_folder='../static', url_prefix='/staff')

    staff_routes.add_url_rule('/work-view', view_func=c.staff_work, methods=['GET'])

    app.register_blueprint(staff_routes)