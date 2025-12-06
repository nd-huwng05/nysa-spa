from flask import Blueprint
from app.core.environment import Environment
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config:ModuleConfig, env:Environment):
    c = Controller(service=service, config=config, env=env)

    user_routes = Blueprint('user', __name__, template_folder='../templates', static_folder='../static', url_prefix='/user')
    user_routes.before_app_request(c.middleware_load_user)
    user_routes.app_context_processor(c.push_data_to_template)

    user_routes.add_url_rule('/login', view_func=c.login, methods=['GET'])
    user_routes.add_url_rule('/auth_user_pass', view_func=c.auth_user_pass, methods=['POST'])
    user_routes.add_url_rule('/auth_google', view_func=c.auth_google, methods=['GET'])
    user_routes.add_url_rule('/logout', view_func=c.logout, methods=['GET'])
    user_routes.add_url_rule('/google/callback', view_func=c.google_callback, methods=['GET'])

    app.register_blueprint(user_routes)