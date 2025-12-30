import copy
import uuid
from datetime import datetime, timedelta
from decimal import Decimal

from ..config.config_module import BookingConfig
from ..repository.repo import Repository

class Service:
    def __init__(self, repo:Repository, config:BookingConfig, env):
        self.repo = repo
        self.config = config
        self.env = env

    def get_staff_appointment(self, staffs, start: datetime, end: datetime, limit_appointment: int):
        staff_ids = [s.id for s in staffs]
        staff_ids_overlimit = self.repo.get_staff_overlimit(start.date(), limit_appointment)
        staff_ids_appointments = self.repo.get_staff_appointment(staff_ids, start, end)
        staff_unsuitable = list(set(staff_ids_overlimit + staff_ids_appointments))
        staff = [s.to_json() for s in staffs if s.id not in staff_unsuitable]
        return staff

    def get_available_staff(self, start_time, end_time, limit_appt):
        staffs = self.env.modules.staff_module.service.get_staff_calendar(start_time, end_time)
        if not staffs:
            return []
        return self.get_staff_appointment(staffs, start_time, end_time, limit_appt)

    def process_booking_timeline(self, service_ids, start_dt, take_staff=True):
        time_rest = self.config.private_config.get("TIME_REST")
        limit_appt = self.config.private_config.get("LIMIT_APPOINTMENTS")

        raw_services = self.env.modules.service_module.service.get_list_services_by_ids(service_ids)
        service_map = {s.id: s for s in raw_services}

        processed_services = []
        total_price = 0
        cursor = start_dt

        for sid in service_ids:
            if sid not in service_map:
                continue

            raw_s = service_map[sid]
            if getattr(raw_s, 'type', None) and raw_s.type.value == "combo":
                _ = list(raw_s.included_services)

            s = copy.deepcopy(raw_s)
            s.start_time = cursor
            total_price += s.price

            if getattr(s, 'type', None) and s.type.value == "combo":
                child_cursor = s.start_time
                last_child_end = s.start_time

                for child in s.included_services:
                    child.start_time = child_cursor
                    child.end_time = child_cursor + timedelta(minutes=child.duration_minutes)
                    child.display_time = f"{child.start_time.strftime('%H:%M')} - {child.end_time.strftime('%H:%M')}"
                    if take_staff:
                        child.staffs = self.get_available_staff(child.start_time, child.end_time, limit_appt)

                    last_child_end = child.end_time
                    child_cursor = child.end_time + timedelta(minutes=time_rest)

                s.end_time = last_child_end
            else:
                s.end_time = s.start_time + timedelta(minutes=s.duration_minutes)

            s.display_time = f"{s.start_time.strftime('%H:%M')} - {s.end_time.strftime('%H:%M')}"
            if take_staff:
                s.staffs = self.get_available_staff(s.start_time, s.end_time, limit_appt)
            processed_services.append(s)
            cursor = s.end_time + timedelta(minutes=time_rest)

        return processed_services, total_price

    def check_staff_appointment(self, data):
        for d in data:
            ok = self.repo.check_staff_appointment(d)
            if not ok:
                raise ValueError("CALENDER WAS BOOKED BY ORDER PERSON, YOU NEED RELOAD PAGE")

    def create_booking(self, booking_date, services, booking_details, customer, data):
        try:
            booking_code = f"BK{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:4].upper()}"
            total_price = sum(s.price for s in services)
            expires_at = booking_date + timedelta(minutes=self.config.private_config.get("RESERVER"))
            booking_id = self.repo.create_booking(booking_code, booking_date, total_price, customer, expires_at)

            extracted_details = []
            for bd in booking_details:
                extracted_details.append({
                    "staff_id": bd['parent']['staff_id'],
                    "start": bd['parent']['start'],
                    "end": bd['parent']['end'],
                })
                for sub in bd['children']:
                    extracted_details.append({
                        "staff_id": sub.get('staff_id'),
                        "start": sub.get('start'),
                        "end": sub.get('end'),
                    })

            self.env.modules.staff_module.service.check_staff_calendar(extracted_details)
            self.check_staff_appointment(extracted_details)

            if not booking_details:
                raise ValueError("DON'T HAVE SERVICE")

            self.repo.create_booking_details(booking_id, booking_details)
            if data.get("voucher_code"):
                voucher_code = data["voucher_code"]
                self.env.modules.voucher_module.service.check_voucher(voucher_code, customer.id, total_price)
                voucher_use = self.env.modules.voucher_module.service.get_voucher_by_code(voucher_code)
                voucher = {
                    "customer_id": customer.id,
                    "voucher_id": voucher_use.id,
                    "discount_amount": Decimal(total_price*voucher_use.discount_value/100) if voucher_use.discount_type.value == "PERCENT" else voucher_use.discount_value,
                    "booking_id": booking_id,
                }
                self.env.modules.voucher_module.service.create_voucher_usage(voucher)

            self.repo.db.session.commit()
            return booking_code
        except Exception as e:
            self.repo.db.session.rollback()
            raise e

    def get_booking_by_code(self, code):
        return self.repo.get_booking_by_code(code)