from ..service.service import Service

class Handler:
    def __init__(self, service:Service, env):
        self.service = service
        self.env = env

    def update(self):
        return self.service.update()

