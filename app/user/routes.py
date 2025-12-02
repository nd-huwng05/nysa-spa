from app import app
from . import controller
from flask import Blueprint

def register_routes():
    user_routes = Blueprint('user', __name__, template_folder='../templates', static_folder='../templates/assets', url_prefix='/user')
    user_routes.app_context_processor(controller.load_logged_in_user)

    user_routes.add_url_rule('/login', view_func=controller.login, methods=['GET', 'POST'])
    user_routes.add_url_rule('/register',  view_func=controller.register, methods=['POST'])
    user_routes.add_url_rule('/logout', view_func=controller.logout, methods=['GET'])
    user_routes.add_url_rule('/refresh', view_func=controller.refresh, methods=['POST'])
    user_routes.add_url_rule('/login/google',view_func=controller.login_google, methods=['GET'])
    user_routes.add_url_rule('/google/callback', view_func=controller.google_auth, methods=['GET'], endpoint='google_auth')


    app.register_blueprint(user_routes)