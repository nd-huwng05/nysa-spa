import re
from datetime import datetime

from flask_login import current_user
from app.utils.validation import validate_datetime
from ..config.config_module import BookingConfig
from ..service.service import Service

class Handler:
    def __init__(self, config: BookingConfig, service: Service, env):
        self.config = config
        self.service = service
        self.env = env

    def _get_service_ids(self, source):
        ids_str = source.get('service_ids') or source.get('service')
        if not ids_str:
            raise ValueError('YOU NEED CHOOSE A SERVICE')
        if isinstance(ids_str, list):
            return [int(x) for x in ids_str]
        return [int(x) for x in ids_str.split(',') if x.strip()]

    def get_data_for_booking(self, request):
        service_ids = request.args.getlist('service')
        if not service_ids:
            return ValueError('YOU NEED CHOOSE A SERVICE')

        services = self.env.modules.service_module.service.get_list_services_by_ids(service_ids)
        total_price = sum(s.price for s in services)
        vouchers = self.env.modules.voucher_module.service.get_list_voucher_customer(current_user.customer.id, total_price)

        return {
            'services': services,
            'customer': current_user.customer if current_user.customer else None,
            'vouchers': vouchers,
            'total_price': total_price,
            'check': None
        }

    def get_appointment_staff(self, request):
        date_str = request.args.get('booking_date')
        time_str = request.args.get('booking_time')
        service_ids = self._get_service_ids(request.args)

        if not date_str or not time_str:
            raise ValueError('YOU NEED CHOOSE TIME')

        start_dt = validate_datetime(date_str, time_str)

        services, total_price = self.service.process_booking_timeline(service_ids, start_dt )

        return {
            "services": services,
            "total_price": total_price,
            "booking_date": start_dt.strftime("%A, %d %B %Y"),
            "booking_time": time_str,
            "customer": current_user.customer if current_user.customer else None,
            'check': True
        }

    def parse_booking_data_final(self, form_data, booking_date_obj):
        date_str = booking_date_obj.strftime("%Y-%m-%d")
        booked_groups = {}
        time_regex = r"(\d{1,2}:\d{2})"

        for key, value in form_data.items():
            if key.startswith("staff-"):
                parts = key.split("-")
                p_idx = parts[1]
                s_id = parts[2]
                s_type = parts[-1]

                times = re.findall(time_regex, key)
                start_dt = end_dt = None
                if len(times) >= 2:
                    start_dt = datetime.strptime(f"{date_str} {times[0]}", "%Y-%m-%d %H:%M")
                    end_dt = datetime.strptime(f"{date_str} {times[1]}", "%Y-%m-%d %H:%M")

                if p_idx not in booked_groups:
                    booked_groups[p_idx] = {"parent": {}, "children": []}

                booked_groups[p_idx]["parent"] = {
                    "service_id": int(s_id),
                    "staff_id": int(value) if value and str(value).isdigit() else None,
                    "type": s_type,
                    "start": start_dt,
                    "end": end_dt
                }

            elif key.startswith("child-"):
                parts = key.split("-")
                p_idx = parts[1]
                child_id = parts[2]

                times = re.findall(time_regex, key)
                c_start = c_end = None
                if len(times) >= 2:
                    c_start = datetime.strptime(f"{date_str} {times[-2]}", "%Y-%m-%d %H:%M")
                    c_end = datetime.strptime(f"{date_str} {times[-1]}", "%Y-%m-%d %H:%M")

                if p_idx not in booked_groups:
                    booked_groups[p_idx] = {"parent": {}, "children": []}

                booked_groups[p_idx]["children"].append({
                    "service_id": int(child_id),
                    "staff_id": int(value) if value and str(value).isdigit() else None,
                    "start": c_start,
                    "end": c_end
                })

        sorted_indices = sorted(booked_groups.keys(), key=int)
        return [booked_groups[idx] for idx in sorted_indices]

    def handler_create_booking(self, request):
        date_str = request.form.get('booking_date')
        time_str = request.form.get('booking_time')
        service_ids = self._get_service_ids(request.form)
        services = self.env.modules.service_module.service.get_list_services_by_ids(service_ids)

        if not services:
            raise ValueError('YOU NEED CHOOSE SERVICES')

        if not date_str or not time_str:
            raise ValueError('YOU NEED CHOOSE A DATE')

        start_dt = validate_datetime(date_str, time_str)

        booking_details = self.parse_booking_data_final(request.form, start_dt)

        return self.service.create_booking(start_dt, services, booking_details, current_user.customer ,request.form)