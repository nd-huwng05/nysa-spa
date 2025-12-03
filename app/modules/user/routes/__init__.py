from flask import Blueprint
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config:ModuleConfig):
    c = Controller(service=service, config=config)

    user_routes = Blueprint('user', __name__, template_folder='../templates', static_folder='../static', url_prefix='/user')
    user_routes.app_context_processor(c.load_logged_in_user)

    user_routes.add_url_rule('/login', view_func=c.login, methods=['GET', 'POST'])
    user_routes.add_url_rule('/logout', view_func=c.logout, methods=['GET'])
    user_routes.add_url_rule('/login/google', view_func=c.google_redirect, methods=['GET'])
    user_routes.add_url_rule('/google/callback', view_func=c.google_auth, methods=['GET'], endpoint='google_auth')

    app.register_blueprint(user_routes)