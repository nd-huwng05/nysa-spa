from app.core.environment import Environment
from .models import Setting


class Repository:
    def __init__(self, env: Environment):
        self.env = env
        self.db = self.env.db

    def get_data_setting_all(self):
        return Setting.query.all()


