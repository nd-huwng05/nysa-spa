from flask import Blueprint
from ..config.config_module import ModuleConfig
from .controller import Controller

def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    invoice_routes = Blueprint('invoice', __name__, template_folder='../templates', static_folder='../static', url_prefix='/invoice')


    invoice_routes.add_url_rule('/payment', view_func=c.invoice_view, methods=['GET'])
    invoice_routes.add_url_rule('/update', view_func=c.update_invoice, methods=['POST'])
    invoice_routes.add_url_rule('/payment/webhook', view_func=c.sepay_webhook, methods=['POST'])
    invoice_routes.add_url_rule('/check-status/<invoice_code>', view_func=c.check_status, methods=['GET'])
    app.register_blueprint(invoice_routes)