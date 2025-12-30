from ..repository.repo import Repository

class Service:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_data_setting(self):
        return self.repo.get_data_setting_all()

    def update(self):
        pass