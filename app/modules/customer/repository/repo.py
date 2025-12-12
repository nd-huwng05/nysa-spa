from flask import g

from app.modules.customer.repository.models import Customer


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db
