from flask import Blueprint
from . import controller
from app import app

def register_routes():
    home_routes = Blueprint('home', __name__, template_folder='../templates', static_folder='../templates/assets', url_prefix='/')

    public_routes = Blueprint('public', __name__, url_prefix='/')
    private_routes = Blueprint('private', __name__, url_prefix='/')



    home_routes.register_blueprint(public_routes)
    home_routes.register_blueprint(private_routes)

    public_routes.add_url_rule('/', endpoint='index', view_func=controller.index)
    app.register_blueprint(home_routes)