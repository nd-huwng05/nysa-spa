from app import app
from . import controller
from flask import Blueprint

def register_routes():
    staff_routes = Blueprint('staff', __name__, template_folder='../templates', static_folder='../templates/assets', url_prefix='/staff')

    public_routes = Blueprint('public', __name__, url_prefix='/')
    private_routes = Blueprint('private', __name__, url_prefix='/')

    staff_routes.register_blueprint(public_routes)
    staff_routes.register_blueprint(private_routes)

    #TO-DO

    app.register_blueprint(staff_routes)