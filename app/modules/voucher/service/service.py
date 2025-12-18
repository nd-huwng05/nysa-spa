from app.core.errors import NewError
from ..repository.repo import Repository


class Service:
    def __init__(self, repo:Repository, config):
        self.repo = repo
        self.config = config

    def get_list_voucher_customer(self,customer_id, total_price):
        voucher = self.repo.get_voucher_global_for_customer(customer_id, total_price)
        return voucher

    def check_voucher(self, voucher_id):
        limit_per_user = self.repo.get_limit_per_user_by_voucher(voucher_id)
        ok = self.repo.check_voucher_by_id(voucher_id, limit_per_user)
        if not ok:
            raise NewError(400,"VOUCHER NOT FOUND, YOU NEED RELOAD PAGE")

