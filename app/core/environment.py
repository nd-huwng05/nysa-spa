from app.extensions import db, jwt, oauth
from app.core.logger import logger


class Environment:
    def __init__(self):
        self.db = db
        self.jwt = jwt
        self.oauth = oauth
        self.app = None

    def init_app(self, app):
        self.app = app
        logger.setup(self.app)
        logger.info("Environment initializing...")
        try:
            self.db.init_app(app)
            logger.info("Database connected successfully")

            self.jwt.init_app(app)
            self.oauth.init_app(app)
            logger.info("Google OAuth Initialized")
        except Exception as e:
            logger.error("Environment init failed", data=str(e))
