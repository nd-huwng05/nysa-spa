from app.core.environment import Environment
from app.modules.service.repository.models import Category, Badge


class Repository:
    def __init__(self, env: Environment):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_all_category():
        return Category.query.all()

    @staticmethod
    def get_all_badge():
        return Badge.query.all()
