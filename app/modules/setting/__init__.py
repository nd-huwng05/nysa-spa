from .repository.repo import Repository
from .service.service import Service
from app.core.environment import Environment

class SettingModule:
    def __init__(self, app, env: Environment):
        self.app = app
        self.env = env
        repo = Repository(env)
        self.service = Service(repo=repo)
        self._observer = []

    def attach(self, observer):
        if observer not in self._observer:
            self._observer.append(observer)

    def notify(self):
        for observer in self._observer:
            observer.update(self)


