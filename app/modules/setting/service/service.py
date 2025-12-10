from ..repository.repo import Repository

class Service:
    def __init__(self, repo: Repository):
        self.repo = repo

