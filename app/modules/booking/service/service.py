from datetime import datetime

from app.core.errors import NewError
from app.core.logger import logger
from ..repository.models import Booking, BookingDetail
from ..repository.repo import Repository

class Service:
    def __init__(self, repo:Repository, config, env):
        self.repo = repo
        self.config = config
        self.env = env

    def get_staff_appointment(self,staffs, start:datetime, end:datetime, limit_appointment:int):
        staff_ids = [s.id for s in staffs]
        staff_ids_overlimit = self.repo.get_staff_overlimit(start.date(), limit_appointment)
        staff_ids_appointments = self.repo.get_staff_appointment(staff_ids, start, end)
        staff_unsuitable = list(set(staff_ids_overlimit + staff_ids_appointments))
        staff = [s.to_json() if s.id not in staff_unsuitable else None for s in staffs]
        return staff

    def check_staff_appointment(self, data):
        for d in data:
            ok = self.repo.check_staff_appointment(d)
            if not ok:
                raise NewError(400, "CALENDER WAS BOOKED BY ORDER PERSON, YOU NEED RELOAD PAGE")

    def add_booking(self, booking:Booking, booking_details, voucher):
        try:
            booking_id, booking_code = self.repo.create_booking(booking)
            self.repo.create_booking_details(booking_id, booking_details)
            if voucher:
                voucher['booking_id'] = booking_id
                self.env.modules.voucher_module.service.create_voucher_usage(voucher)
            self.repo.db.session.commit()
            return {
                "booking_id": booking_id,
                "booking_code": booking_code,
            }
        except Exception as e:
            self.repo.db.session.rollback()
            logger.error("ERROR ADD BOOKING", data=str(e))
            raise NewError(500,"ERROR CAN'T ADD BOOKING")

    def get_booking_by_id(self, booking_id):
        return self.repo.get_booking_by_id(booking_id)

    def update_payment_booking(self, booking_id, payment_type):
        try:
            self.repo.update_payment_booking(booking_id, payment_type)
            self.repo.db.session.commit()
        except Exception as e:
            return NewError(500,"ERROR CAN'T UPDATE PAYMENT BOOKING")