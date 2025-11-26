from app import app
from . import controller
from flask import Blueprint

def register_routes():
    user_routes = Blueprint('user', __name__, template_folder='../templates', static_folder='../templates/assets', url_prefix='/user')

    public_routes = Blueprint('public', __name__, url_prefix='/')
    private_routes = Blueprint('private', __name__, url_prefix='/')

    user_routes.register_blueprint(public_routes)
    user_routes.register_blueprint(private_routes)

    public_routes.add_url_rule('/login', endpoint='login', view_func=controller.login)
    app.register_blueprint(user_routes)