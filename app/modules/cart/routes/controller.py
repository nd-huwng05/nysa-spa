from flask import abort, render_template, redirect, url_for, flash, session, jsonify
from app.core.logger import logger
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    def cart_view(self):
        cart_items = self.handler.get_service_cart()
        return render_template('page/cart_view.html', cart_items=cart_items)

    def push_count_service(self):
        try:
            return self.handler.push_count_service()
        except Exception as e:
            logger.info("Can't push count service: {}".format(e))
            abort(500)

    def add_service_item(self, item_id):
        return self.handler.add_service_item(item_id)


    def remove_service_item(self, item_id):
        return self.handler.remove_service_item(item_id)
