from app import app
from . import controller
from flask import Blueprint

def register_routes():
    service_routes = Blueprint('service', __name__, template_folder='../templates', static_folder='../templates/assets', url_prefix='/service')

    public_routes = Blueprint('public', __name__, url_prefix='/')
    private_routes = Blueprint('private', __name__, url_prefix='/')

    service_routes.register_blueprint(public_routes)
    service_routes.register_blueprint(private_routes)

    #TO-DO

    app.register_blueprint(service_routes)