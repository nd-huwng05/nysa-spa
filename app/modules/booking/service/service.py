from datetime import datetime

from ..repository.repo import Repository

class Service:
    def __init__(self, repo:Repository, config):
        self.repo = repo
        self.config = config

    def get_staff_appointment(self,staffs, start:datetime, end:datetime, limit_appointment:int):
        staff_ids = [s.id for s in staffs]
        staff_ids_overlimit = self.repo.get_staff_overlimit(start.date(), limit_appointment)
        staff_ids_appointments = self.repo.get_staff_appointment(staff_ids, start, end)
        staff_unsuitable = list(set(staff_ids_overlimit + staff_ids_appointments))
        staff = [s.to_json() if s.id not in staff_unsuitable else None for s in staffs]
        return staff

