class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

