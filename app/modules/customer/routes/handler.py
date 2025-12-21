from flask import Request

from app.core.logger import logger
from app.core.errors import NewError, NewPackage
from ..service.service import Service
from ..utils.validation import validate_email, validate_phone


class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env

    def update_info(self, request: Request):
        try:
            data = request.get_json()
            if not data or 'id' not in data:
                raise NewError(400, "DATA INVALID")

            errors = self.service.update_customer_info(data)
            if errors:
                raise NewError(400, errors)
            return NewPackage(message="UPDATE SUCCESS").response()
        except ValueError as e:
            raise NewError(404, str(e))
        except Exception as e:
            logger.error("Can't update customer info", data=str(e))
            raise NewError(500, str(e))

    def search(self, request: Request):
        try:
            data = request.args.get("data")
            customer = self.service.search_customer(data)
            return NewPackage(customer).response()
        except Exception as e:
            logger.error("Can't search customer info", data=str(e))
            raise NewError(500, str(e))

    def create(self, request: Request):
        try:
            data = request.get_json()
            if not data:
                raise NewError(400, "DATA INVALID")

            email = data.get("email")
            if not validate_email(email):
                raise NewError(400, "EMAIL INVALID")

            phone = data.get("phone")
            if not validate_phone(phone):
                raise NewError(400, "PHONE INVALID")

            fullname = data.get("fullname")
            if not fullname:
                raise NewError(400, "FULLNAME INVALID")
            errors = self.service.create_customer(data)
            if errors:
                raise NewError(400, errors)
            return NewPackage(message="CREATE SUCCESS").response()
        except Exception as e:
            logger.error("Can't create customer info", data=str(e))
            raise NewError(500, "INTERNAL SERVER ERROR")