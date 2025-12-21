from flask import Blueprint
from .controller import Controller


def register_routes(app, service, config, env):
    c = Controller(service=service, config=config, env=env)

    service_routes = Blueprint('service', __name__, template_folder='../templates', static_folder='../static', url_prefix='/service')


    service_routes.add_url_rule('/service-search', view_func=c.service_search_view, methods=['GET'])
    service_routes.add_url_rule('/list', view_func=c.get_list_service, methods=['GET'])
    service_routes.add_url_rule('/service-details-view', view_func=c.service_detail_view, methods=['GET'])
    service_routes.add_url_rule('/search', view_func=c.search_json, methods=['GET'])
    app.register_blueprint(service_routes)