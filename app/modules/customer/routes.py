from app import app
from . import controller
from flask import Blueprint

def register_routes():
    customer_routes = Blueprint('customer', __name__, template_folder='../templates', static_folder='../templates/assets', url_prefix='/customer')

    public_routes = Blueprint('public', __name__, url_prefix='/')
    private_routes = Blueprint('private', __name__, url_prefix='/')

    customer_routes.register_blueprint(public_routes)
    customer_routes.register_blueprint(private_routes)

    #TO-DO

    app.register_blueprint(customer_routes)