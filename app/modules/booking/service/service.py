from app.core.logger import logger
from ..repository.repo import Repository

class Service:
    def __init__(self, repo:Repository, config):
        self.repo = repo
        self.config = config

    def get_booking_by_id(self, booking_id, customer_id):
        try:
            return self.repo.get_booking_by_id(booking_id, customer_id)
        except Exception as e:
            logger.error("Can't get booking by id {} {}".format(booking_id, e))
            raise Exception("Get data booking fails")