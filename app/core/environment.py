from types import SimpleNamespace
from pymysql import OperationalError
from sqlalchemy import text
from app.extensions import db, jwt, oauth, migrate
from app.core.logger import logger


class Environment:
    def __init__(self):
        self.db = db
        self.jwt = jwt
        self.oauth = oauth
        self.migrate = migrate
        self.app = None
        self.modules = SimpleNamespace()

    def init_app(self, app):
        self.app = app
        logger.setup(self.app)
        logger.info("Environment initializing...")
        try:
            self.db.init_app(app)
            self._exam_connect_database()
            logger.info("Database connected successfully")

            self.jwt.init_app(app)
            self.oauth.init_app(app)
            logger.info("Google OAuth Initialized")

            self.migrate.init_app(app=app, db=self.db)
        except Exception as e:
            logger.error("Environment init failed", data=str(e))
            exit(1)

    def add_module(self, key:str, module):
        setattr(self.modules, key, module)

    def _exam_connect_database(self):
        try:
            with self.app.app_context():
                with self.db.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
        except OperationalError as e:
            raise OperationalError(str(e))
