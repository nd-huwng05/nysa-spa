from flask import Blueprint

from app.core.middleware import jwt_middleware
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    voucher_routes = Blueprint('voucher', __name__, template_folder='../templates', static_folder='../static', url_prefix='/voucher')


    voucher_routes.add_url_rule('/', view_func=c.index, methods=['GET'])
    voucher_routes.add_url_rule('load', view_func=c.voucher_suitable, methods=['GET'])

    app.register_blueprint(voucher_routes)