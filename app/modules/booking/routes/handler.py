import uuid
from datetime import timedelta, datetime
from decimal import Decimal

from flask import g, Request

from app.core.errors import NewError, NewPackage
from app.utils.validation import validate_datetime
from ..config.config_module import BookingConfig
from ..repository.models import Booking, BookingDetail
from ..service.service import Service


class Handler:
    def __init__(self, config: BookingConfig, service: Service, env):
        self.config = config
        self.service = service
        self.env = env

    def handler_book_view(self, request: Request):
        service_ids = request.args.getlist('service')
        if not service_ids:
            return None, "You need choose least one service"

        services = self.env.modules.service_module.service.get_list_services_by_ids(service_ids)
        customer = None
        if g.current_user.role.value == "CUSTOMER":
            customer = g.current_user.customer

        return {
            "services": services,
            "customer": customer
        }, None

    def handler_staff_appointment(self, request: Request):
        day = request.args.get('start')
        duration = request.args.get('duration', type=int)
        start = validate_datetime(day)
        end = start + timedelta(minutes=duration)
        staffs = self.env.modules.staff_module.service.get_staff_calendar(start, end)
        if not staffs:
            return {
                "staff_appointment": None
            }
        end = end + timedelta(minutes=self.config.private_config.get('TIME_REST'))
        staff_appointment = self.service.get_staff_appointment(staffs, start, end,
                                                               self.config.private_config.get('LIMIT_APPOINTMENTS'))
        return {
            "staff_appointment": staff_appointment
        }

    def handler_booking_voucher(self, request: Request):
        customer_id = 1
        if g.current_user.role.value == "CUSTOMER":
            customer_id = g.current_user.customer.id

        email = request.args.get('email')
        if not email:
            raise NewError(400, "You need enter email")

        total_price = request.args.get('total_price', type=Decimal)
        if not total_price:
            raise NewError(400, "TOTAL_PRICE IS REQUIRED")
        vouchers = self.env.modules.voucher_module.service.get_list_voucher_customer(customer_id, total_price)
        return vouchers

    def handler_add_booking(self, request: Request):
        data = request.json
        booking_time = data.get('booking_time')
        booking_time = validate_datetime(booking_time)
        if not booking_time:
            raise NewError(400, "BOOKING_TIME IS REQUIRED")

        customer_id = data.get('customer_id')
        if not customer_id:
            raise NewError(400, "CUSTOMER IS REQUIRED")

        notes = data.get('notes')
        booking_code = f"BK{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:4].upper()}"

        total_amount = data.get('total_amount')
        if not total_amount:
            raise NewError(400, "TOTAL_AMOUNT IS REQUIRED")

        expires = booking_time + timedelta(minutes=self.config.private_config.get('EXPIRES_PENDING'))

        booking = Booking(
            booking_code=booking_code,
            customer_id=customer_id,
            booking_time=booking_time,
            total_amount=total_amount,
            expires_at=expires,
            notes=notes
        )

        voucher_id = data.get('voucher_id', None)
        if voucher_id and voucher_id != '':
            self.env.modules.voucher_module.service.check_voucher(voucher_id)
            booking.voucher_id = int(voucher_id)

        details = data.get('details')
        if not details:
            raise NewError(400, "NO SEE SERVICE DETAILS")

        extracted_details = []
        for d in details:
            extracted_details.append({
                "staff_id": d.get('staff_id'),
                "start": d.get('start'),
                "end": d.get('end'),
            })

            sub_details = d.get('sub_detail', [])
            for sub in sub_details:
                extracted_details.append({
                    "staff_id": sub.get('staff_id'),
                    "start": sub.get('start'),
                    "end": sub.get('end'),
                })

        self.env.modules.staff_module.service.check_staff_calendar(extracted_details)
        self.service.check_staff_appointment(extracted_details)

        result = self.service.add_booking(booking, details)
        return NewPackage(result).response()
