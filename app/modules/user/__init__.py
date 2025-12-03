from .routes.handler import Handler
from .repository.repo import Repository
from .config.config_module import ModuleConfig
from .routes.controller import Controller
from .service.service import Service
from .routes import register_routes
from app.core.environment import Environment


class UserModule:
    def __init__(self, app, env: Environment):
        self.app = app
        self.config = ModuleConfig(app.config)
        self.env = env
        self._setup_google_oauth()
        repo = Repository(env)
        self.service = Service(repo=repo, config=self.config)

    def register(self):
        register_routes(self.app, self.service, self.config, self.env)

    def _setup_google_oauth(self):
        self.env.oauth.register(
            name='google',
            client_id=self.config.private_config['GOOGLE_CLIENT_ID'],
            client_secret=self.config.private_config['GOOGLE_CLIENT_SECRET'],
            server_metadata_url=self.config.private_config['GOOGLE_SERVER_METADATA_URL'],
            client_kwargs={'scope': self.config.private_config['GOOGLE_CLIENT_SCOPE']}
        )

