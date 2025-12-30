from datetime import date, datetime, timedelta
from decimal import Decimal
from sqlalchemy import func, and_, extract
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

    def create_booking(self, booking_code, booking_date, total_price, customer, expires_at):
        new_booking = Booking(
            booking_code=booking_code,
            booking_time=booking_date,
            customer_id=customer.id,
            status=BookingStatus.PENDING.value,
            payment=PaymentStatus.NONE.value,
            total_amount=Decimal(total_price),
            expires_at = expires_at
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

    def get_booking_by_code(self, code):
        return Booking.query.filter(Booking.booking_code == code).first()

    def get_bookings(self, date: datetime):
        bookings = self.db.session.query(Booking).filter(
            func.date(Booking.booking_time) == date
        ).all()
        return bookings

    @staticmethod
    def get_status_booking():
        complete = Booking.query.filter(Booking.status == BookingStatus.COMPLETED.value).count()
        canceled = Booking.query.filter(Booking.status == BookingStatus.CANCELED.value).count()
        booked = Booking.query.filter(Booking.status == BookingStatus.SUCCESS.value).count()

        return {
            'complete': complete,
            'canceled': canceled,
            'booked': booked,
            'total': complete + canceled + booked,
        }

    @staticmethod
    def get_statistical_week():
        start_week = datetime.now() - timedelta(days=datetime.now().weekday())
        week_query = Booking.query.with_entities(
            func.date(Booking.booking_time), func.sum(Booking.total_amount)
        ).filter(
            Booking.booking_time >= start_week,
            Booking.status == 'COMPLETED',
        ).group_by(func.date(Booking.booking_time)).all()

        week_data_arr = [0] * 7
        for date_val, total in week_query:
            d_idx = date_val.weekday() if hasattr(date_val, 'weekday') else datetime.strptime(str(date_val),
                                                                                              '%Y-%m-%d').weekday()
            week_data_arr[d_idx] = float(total)

        return week_data_arr

    @staticmethod
    def get_statistical_month():
        start_month = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        month_query = Booking.query.filter(
            Booking.booking_time >= start_month,
            Booking.status == 'COMPLETED',
        ).all()

        month_data_arr = [0] * 4
        for booking in month_query:
            day = booking.booking_time.day
            if day <= 7:
                idx = 0
            elif day <= 14:
                idx = 1
            elif day <= 21:
                idx = 2
            else:
                idx = 3

            month_data_arr[idx] += float(booking.total_amount)
        return month_data_arr

    @staticmethod
    def get_statistical_year():
        start_year = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0)
        year_query = Booking.query.with_entities(
            extract('month', Booking.booking_time).label('m'),
            func.sum(Booking.total_amount)
        ).filter(
            Booking.booking_time >= start_year,
            Booking.status == 'completed'
        ).group_by('m').all()

        year_data_arr = [0] * 12
        for m, total in year_query:
            year_data_arr[int(m) - 1] = float(total)
        return year_data_arr

    @staticmethod
    def get_time_gold():
        peak_query = BookingDetail.query.with_entities(
            extract('hour', BookingDetail.start).label('h'),
            func.count(BookingDetail.id)
        ).group_by('h').all()

        peak_dict = {int(h): count for h, count in peak_query}
        peak_data_arr = [peak_dict.get(h, 0) for h in range(8, 18)]

        return peak_data_arr

    @staticmethod
    def get_frequency():
        start_week = datetime.now() - timedelta(days=datetime.now().weekday())
        freq_query = Booking.query.with_entities(
            func.date(Booking.booking_time),
            func.count(Booking.id)
        ).filter(
            Booking.booking_time >= start_week,
            Booking.status.in_(['BOOKED', 'COMPLETED']),
        ).group_by(func.date(Booking.booking_time)).all()
        frequency_data_arr = [0] * 7
        for date_val, count in freq_query:
            d_idx = date_val.weekday() if hasattr(date_val, 'weekday') else datetime.strptime(str(date_val),
                                                                                              '%Y-%m-%d').weekday()
            frequency_data_arr[d_idx] = int(count)
        return frequency_data_arr