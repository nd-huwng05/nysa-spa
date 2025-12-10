from flask import Blueprint
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    booking_routes = Blueprint('booking', __name__, template_folder='../templates', static_folder='../static', url_prefix='/booking')


    booking_routes.add_url_rule('/booking_view', view_func=c.book_view, methods=['GET'])

    app.register_blueprint(booking_routes)