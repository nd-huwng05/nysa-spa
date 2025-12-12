from ..repository.repo import Repository
from app.core.logger import logger

class Service:
    def __init__(self, repo:Repository, config):
        self.repo = repo
        self.config = config

    def get_voucher_by_id(self, voucher_id):
        try:
            return self.repo.get_voucher_by_id(voucher_id)
        except Exception as e:
            logger.error("Can't get voucher by id {} {}".format(voucher_id, e))
            raise Exception("Get data voucher fails")

