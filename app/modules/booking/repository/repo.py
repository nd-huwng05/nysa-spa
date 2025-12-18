from datetime import datetime, date
from sqlalchemy import and_, func

from .models import BookingDetail, Booking


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_staff_appointment(staff_ids, start:datetime, end:datetime):
        filters = and_(
            BookingDetail.staff_id.in_(staff_ids),
            BookingDetail.start <= end,
            BookingDetail.end >= start,
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

    @staticmethod
    def check_staff_appointment(data):
        filters = and_(
            BookingDetail.staff_id == data.get("staff_id"),
            BookingDetail.start <= data.get("end"),
            BookingDetail.end >= data.get("start"),
        )
        appointments = BookingDetail.query.filter(filters).first()
        if appointments:
            return False
        return True

    def create_booking(self, booking:Booking):
        self.db.session.add(booking)
        self.db.session.flush()
        return booking.id, booking.booking_code

    def create_booking_details(self,booking_id:int, booking_details):
        for booking_detail in booking_details:
            parent = BookingDetail(
                booking_id=booking_id,
                service_id=booking_detail.get('service_id'),
                staff_id=booking_detail.get('staff_id'),
                start=booking_detail.get('start'),
                end=booking_detail.get('end'),
                price=booking_detail.get('price'),
            )
            self.db.session.add(parent)
            self.db.session.flush()

            sub = booking_detail.get('sub_detail', [])
            if sub:
                for sub_detail in sub:
                    child = BookingDetail(
                        booking_id=booking_id,
                        service_id=sub_detail.get('service_id'),
                        staff_id=sub_detail.get('staff_id'),
                        start=sub_detail.get('start'),
                        end=sub_detail.get('end'),
                        price=sub_detail.get('price'),
                        parent_id=parent.id,
                    )

                    self.db.session.add(child)

    @staticmethod
    def get_booking_by_id(id:int):
        return Booking.query.get(id)

