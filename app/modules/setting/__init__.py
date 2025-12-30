from .repository.repo import Repository
from .routes import register_routes
from .service.service import Service
from app.core.environment import Environment

class SettingModule:
    def __init__(self, app, env: Environment):
        self.app = app
        self.env = env
        repo = Repository(env)
        self.service = Service(repo=repo)
        self._observer = []

    def register_routes(self):
        register_routes(self.app, self.service, self.env)

    def get_settings_data(self):
        return self.service.get_data_setting()

    def handle_setting_change(self):
        self.notify()

    def attach(self, observer):
        if observer not in self._observer:
            self._observer.append(observer)

    def notify(self):
        for observer in self._observer:
            observer.update(self)