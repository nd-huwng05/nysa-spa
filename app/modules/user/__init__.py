from .routes.handler import Handler
from .repository.repo import Repository
from .config.config_module import UserConfig
from .routes.controller import Controller
from .service.service import Service
from .routes import register_routes
from app.core.environment import Environment
from ...core.interface import IModule


class UserModule(IModule):
    def __init__(self, app, env: Environment):
        super().__init__(app, env, module_name="user_module")
        self.config = UserConfig(app.config)
        self._setup_google_oauth()
        repo = Repository(env)
        self.service = Service(repo=repo, config=self.config)

    def _register_routes(self):
        register_routes(self.app, self.service, self.config, self.env)

    def _setup_google_oauth(self):
        self.env.oauth.register(
            name='google',
            client_id=self.config.GOOGLE_CLIENT_ID,
            client_secret=self.config.GOOGLE_CLIENT_SECRET,
            server_metadata_url=self.config.GOOGLE_SERVER_METADATA_URL,
            client_kwargs={'scope': self.config.GOOGLE_CLIENT_SCOPE}
        )

