from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import func, and_

from .models import BookingDetail, Booking, BookingStatus, PaymentStatus


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_staff_overlimit(day: date, limit: int):
        count_bookings = func.count(BookingDetail.id)
        staff_ids = BookingDetail.query.filter(func.date(BookingDetail.create_at) == day).group_by(
            BookingDetail.staff_id).having(count_bookings >= limit).with_entities(BookingDetail.staff_id).all()
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

    @staticmethod
    def get_staff_appointment(staff_ids, start: datetime, end: datetime):
        filters = and_(
            BookingDetail.staff_id.in_(staff_ids),
            BookingDetail.start <= end,
            BookingDetail.end >= start,
        )
        appointments = BookingDetail.query.filter(filters)
        staff_ids = appointments.with_entities(BookingDetail.staff_id).distinct().all()
        staff_ids = [i for (i,) in staff_ids]
        return staff_ids

    def create_booking(self, booking_code, booking_date, total_price, customer):
        new_booking = Booking(
            booking_code=booking_code,
            booking_time=booking_date,
            customer_id=customer.id,
            status=BookingStatus.PENDING.value,
            payment=PaymentStatus.NONE.value,
            total_amount=Decimal(total_price),
        )
        self.db.session.add(new_booking)
        self.db.session.flush()
        return new_booking.id

    def create_booking_details(self, booking_id, booking_details):
        for detail in booking_details:
            parent_data = detail['parent']

            booking_detail = BookingDetail(
                booking_id=booking_id,
                service_id=parent_data['service_id'],
                staff_id=parent_data['staff_id'],
                start=parent_data['start'],
                end=parent_data['end'],
                price=parent_data.get('price', 0)
            )
            self.db.session.add(booking_detail)
            self.db.session.flush()

            if detail.get('children'):
                for child in detail['children']:
                    new_child = BookingDetail(
                        booking_id=booking_id,
                        service_id=child['service_id'],
                        staff_id=child['staff_id'] if child['staff_id'] else parent_data['staff_id'],
                        start=child['start'],
                        end=child['end'],
                        price=0,
                        parent_id=booking_detail.id
                    )
                    self.db.session.add(new_child)