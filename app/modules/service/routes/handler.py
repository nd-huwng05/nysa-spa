from app.utils.pagination import Pagination
from ..config.config_module import ServiceConfig


class Handler:
    def __init__(self, config:ServiceConfig, service, env):
        self.config = config
        self.service = service
        self.env = env

    def prepare_search_view_data(self):
        category, badge, features = self.service.get_filter_master_data()
        pagination = Pagination(page=1, size=self.config.private_config.get('PAGE_SIZE_FOR_SEARCH'))
        services, pagination = self.service.get_list_services(pagination)
        return {
            'category': category,
            'badge': badge,
            'services': services,
            'pagination': pagination,
            'features': features
        }

    def get_list_service_filter(self, request):
        text_search = request.args.get('search', type=str)
        category_id = request.args.get('category',None, type=int)
        badge_id = request.args.get('badge', None, type=int)
        sort_by = request.args.get('sort', 'newest', type=str)
        feature_id = request.args.get('feature', None, type=int)
        page = request.args.get('page', type=int)
        pagination = Pagination(page=page, size=self.config.private_config.get('PAGE_SIZE_FOR_SEARCH'))

        filter = {
            'text_search': text_search,
            'category_id': category_id,
            'badge_id': badge_id,
            'feature_id': feature_id,
            'sort_by': sort_by,
        }

        services, pagination = self.service.get_list_service_filter(filter, pagination)
        return {
            'services': services,
            'pagination': pagination,
        }






