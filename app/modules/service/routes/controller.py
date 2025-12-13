from flask import abort, render_template, request, flash
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    def service_search_view(self):
        data = self.handler.prepare_search_view_data()
        if data is None:
            flash("500 Internal Server Error", "error")
            return None
        return render_template('page/service_search.html', **data)

    @staticmethod
    def service_detail_view():
        return render_template('page/service_detail.html')

    def get_list_service(self):
        result = self.handler.get_list_service_filter(request)
        print(result)