from .models import Booking

class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_booking_by_id(booking_id, customer_id):
        return Booking.query.filter_by(id=booking_id, customer_id=customer_id).first()
