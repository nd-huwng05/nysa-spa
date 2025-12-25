from flask import Blueprint
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    cart_routes = Blueprint('cart', __name__, template_folder='../templates', static_folder='../static', url_prefix='/cart')
    cart_routes.app_context_processor(c.push_count_service)

    cart_routes.add_url_rule('/cart-view', view_func=c.cart_view, methods=['GET'])
    cart_routes.add_url_rule('/remove/<int:item_id>', view_func=c.remove_service_item, methods=['POST'])
    cart_routes.add_url_rule('/add/<int:item_id>', view_func=c.add_service_item, methods=['POST'])
    cart_routes.add_url_rule('/toggle-check', view_func=c.toggle_check, methods=['POST'])

    app.register_blueprint(cart_routes)