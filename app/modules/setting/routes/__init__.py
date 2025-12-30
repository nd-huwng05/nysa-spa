from flask import Blueprint

from app.core.middleware import login_required, admin_required
from .controller import Controller

def register_routes(app, service, env):
    c = Controller(service=service, env=env)

    setting_routes = Blueprint('setting', __name__, template_folder='../templates', static_folder='../static', url_prefix='/setting')

    setting_routes.add_url_rule('update', view_func=login_required(admin_required(c.update)), methods=['GET'])

    app.register_blueprint(setting_routes)