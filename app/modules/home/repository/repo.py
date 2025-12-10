from app.core.logger import logger
from app.core.environment import Environment
from .models import RoleSection, Section


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db