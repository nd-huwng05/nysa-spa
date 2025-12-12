from app.core.environment import Environment
from .models import Service

class Repository:
    def __init__(self, env: Environment):
        self.env = env
        self.db = self.env.db

    def get_list_services(self, list_id):
        return Service.query.filter(Service.id.in_(list_id)).all()
