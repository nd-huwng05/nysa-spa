from flask import Blueprint
from app.extensions import login_manager
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    user_routes = Blueprint('user', __name__, template_folder='../templates', static_folder='../static', url_prefix='/user')

    user_routes.add_url_rule('/login', view_func=c.login, methods=['GET'])
    user_routes.add_url_rule('/auth_user_pass', view_func=c.auth_user_pass, methods=['POST'])
    user_routes.add_url_rule('/auth_google', view_func=c.auth_google, methods=['GET'])
    user_routes.add_url_rule('/logout', view_func=c.logout, methods=['GET'])
    user_routes.add_url_rule('/google/callback', view_func=c.google_callback, methods=['GET'])

    @login_manager.user_loader
    def load_user(user_id):
        return c.user(user_id)
    app.register_blueprint(user_routes)