from app.core.environment import Environment


class Repository:
    def __init__(self, env: Environment):
        self.env = env
        self.db = self.env.db

