from flask import Request, g

from ..service.service import Service

class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env

    def get_data_for_view(self, request: Request):
        booking_id = request.args.get('booking_id', None)

        if booking_id is None:
            return None, 'BOOKING_ID is required'
        booking = self.env.modules.booking_module.service.get_booking_by_id(booking_id)


        if booking is None:
            return None, 'NOT FOUND BOOKING'

        if booking.status.value != 'PENDING':
            return None, 'Booking is paid or awaiting payment or cancelled'

        return {
            'booking': booking,
            'voucher': booking.voucher_usage.voucher,
            'booking_detail': booking.booking_details,
        }, None