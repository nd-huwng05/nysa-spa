from app.modules.voucher.repository.models import Voucher


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_voucher_by_id(booking_id):
        return Voucher.query.get(booking_id)