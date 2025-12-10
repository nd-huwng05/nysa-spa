from app.core.environment import Environment
from .models import Setting


class Repository:
    def __init__(self, env: Environment):
        self.env = env
        self.db = self.env.db

    def get_all_settings(self):
        return self.db.session.query(Setting).all()

    def get_setting(self, name_module):
        return self.db.session.query(Setting).filter_by(type=name_module).all()

    def save_setting(self, setting: Setting):
        self.db.session.add(setting)
        self.db.session.commit()

