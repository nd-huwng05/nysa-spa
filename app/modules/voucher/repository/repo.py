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
        return Voucher.query.filter_by(id=voucher_id).first().limit_per_user

    @staticmethod
    def check_voucher_by_id(voucher_id, customer_id, total_price, limit_per_user ):
        base_conditions = and_(
            Voucher.active == True,
            Voucher.min_order_value <= total_price,
            Voucher.start_at <= datetime.now(),
            Voucher.end_at >= datetime.now(),
            Voucher.usage_count < Voucher.usage_limit,
            Voucher.scope == VoucherScope.GLOBAL,
            VoucherUsage.voucher_id == voucher_id,
            VoucherUsage.customer_id == customer_id
        )
        usage = VoucherUsage.query.filter(base_conditions).count()
        if usage >= limit_per_user:
            return False
        return True


    def create_voucher_usage(self, voucher):
        usage = VoucherUsage(
            booking_id=voucher.get('booking_id'),
            voucher_id=voucher.get('voucher_id'),
            discount_amount=voucher.get('discount_amount'),
            customer_id=voucher.get('customer_id'),
        )
        self.db.session.add(usage)