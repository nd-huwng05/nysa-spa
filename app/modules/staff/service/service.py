from datetime import datetime

from app.core.errors import NewError
from ..repository.repo import Repository

class Service:
    def __init__(self, repo:Repository, config):
        self.repo = repo
        self.config = config

    def get_staff_calendar(self, start:datetime, end:datetime):
        try:
            staff_ids = self.repo.get_staff_ids_calendar(start, end)
            return self.repo.get_list_staff_by_ids(staff_ids)
        except Exception as e:
            raise NewError(500, "ERROR GET STAFF CALENDAR")

    def check_staff_calendar(self, data):
        for d in data:
            ok = self.repo.check_staff_calendar(d)
            if not ok:
                raise ValueError("ERROR CHOOSE STAFF, YOU NEED RELOAD PAGE")
