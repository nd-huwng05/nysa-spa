from datetime import datetime

from sqlalchemy import func, and_, or_, desc

from .models import Voucher, VoucherScope, VoucherUsage


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    def get_voucher_global_for_customer(self, customer_id:int, total_price: int):
        base_conditions = [
            Voucher.active == True,
            Voucher.min_order_value <= total_price,
            Voucher.start_at <= datetime.now(),
            Voucher.end_at >= datetime.now(),
            Voucher.usage_count < Voucher.usage_limit,
            Voucher.scope == VoucherScope.GLOBAL
        ]

        query = Voucher.query.filter(*base_conditions)
        usage_count_subquery = (
            self.db.session.query(func.count(VoucherUsage.id))
            .filter(VoucherUsage.voucher_id == Voucher.id)
            .filter(VoucherUsage.customer_id == customer_id)
            .correlate(Voucher)
            .scalar_subquery()
        )

        voucher = query.filter(usage_count_subquery < Voucher.limit_per_user).order_by(desc(Voucher.create_at)).all()
        return voucher
    @staticmethod
    def get_limit_per_user_by_voucher(voucher_id:int):
        return Voucher.query.filter_by(voucher_id=voucher_id).first().limit_per_user

    @staticmethod
    def check_voucher_by_id(self, voucher_id, limit_per_user):
        usage = VoucherUsage.query.filter_by(voucher_id=voucher_id).all()
        return usage.count() < limit_per_user