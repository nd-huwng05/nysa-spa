from datetime import datetime, date
from sqlalchemy import and_, func

from app.modules.booking.repository.models import BookingDetail


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_staff_appointment(staff_ids, start:datetime, end:datetime):
        filters = and_(
            BookingDetail.staff_id.in_(staff_ids),
            BookingDetail.start_time <= end,
            BookingDetail.end_time >= start,
        )
        appointments = BookingDetail.query.filter(filters)
        staff_ids = appointments.with_entities(BookingDetail.staff_id).distinct().all()
        staff_ids = [i for (i,) in staff_ids]
        return staff_ids

    @staticmethod
    def get_staff_overlimit(day: date, limit:int):
        count_bookings = func.count(BookingDetail.id)
        staff_ids = BookingDetail.query.filter(func.date(BookingDetail.create_at) == day).group_by(BookingDetail.staff_id).having(count_bookings >= limit).with_entities(BookingDetail.staff_id).all()
        staff_ids = [i for (i,) in staff_ids]
        return staff_ids