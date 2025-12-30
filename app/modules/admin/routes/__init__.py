from flask import Blueprint
from app.core.environment import Environment
from app.core.middleware import login_required, admin_required
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    admin_routes = Blueprint('admin', __name__, template_folder='../templates', static_folder='../static', url_prefix='/admin')


    admin_routes.add_url_rule('/', view_func=login_required(admin_required(c.index)), methods=['GET'])
    admin_routes.add_url_rule('/dashboard', view_func=login_required(admin_required(c.dashboard)), methods=['GET'])
    admin_routes.add_url_rule('/voucher', view_func=login_required(admin_required(c.voucher)), methods=['GET'])
    admin_routes.add_url_rule('settings', view_func=login_required(admin_required(c.settings)), methods=['GET'])
    app.register_blueprint(admin_routes)