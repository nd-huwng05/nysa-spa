from ..config.config_module import ServiceConfig


class Handler:
    def __init__(self, config:ServiceConfig, service, env):
        self.config = config
        self.service = service
        self.env = env

    def prepare_search_view_data(self):
        filter_options = self.service.get_filter_master_data()
        return {
            'filter': filter_options,
        }

    def get_list_service(self, request):
        category_id = request.args.get('category_id', None)
        duration = request.args.get('duration', None)
        badge_id = request.args.get('badge_id', None)
        sort_by = request.args.get('sort_by', None)
        page = request.args.get('page', None)
        per_page = self.config.private_config.get('PER_PAGE', 9)

        if page is None or int(page) > 1:
            page = 1
        if sort_by is None:
            sort_by = "newest"

        filter_data = {
            'category_id': category_id,
            'duration': duration,
            'badge_id': badge_id,
            'sort_by': sort_by,
            'page': page,
            'per_page': per_page
        }

        result = self.service.get_list_service(filter_data)

        return {
            'result': result,
        }






