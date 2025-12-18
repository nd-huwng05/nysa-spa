from datetime import datetime
from sqlalchemy import and_, or_
from .models import Staff, StaffCalendar


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    def get_all_active_staff(self):
        return self.db.session.query(Staff).filter(Staff.is_active == True).all()

    @staticmethod
    def get_staff_ids_calendar(start: datetime, end: datetime):
        filters = and_(
            StaffCalendar.start <= start,
            StaffCalendar.end >= end,
        )
        staff_ids = StaffCalendar.query.filter(filters).with_entities(StaffCalendar.staff_id).distinct().all()
        staff_ids = [i for (i,) in staff_ids]
        return staff_ids

    @staticmethod
    def get_list_staff_by_ids(staff_ids):
        return Staff.query.filter(Staff.id.in_(staff_ids)).all()

    @staticmethod
    def check_staff_calendar(data):
        filters = and_(
            StaffCalendar.staff_id == data.get("staff_id"),
            StaffCalendar.start <= data.get("start"),
            StaffCalendar.end >= data.get("end"),
        )
        staff_calendar = StaffCalendar.query.filter(filters).first()
        if staff_calendar:
            return True
        return False
