from flask import Request

from app import logger
from app.core.errors import NewError, NewPackage
from ..service.service import Service


class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env

    def update_info(self, request: Request):
        try:
            data = request.get_json()
            print(data)
            if not data or 'id' not in data:
                raise NewError(400, "DATA INVALID")

            errors = self.service.update_customer_info(data)
            if errors:
                raise NewError(400, errors)
            return NewPackage(message="UPDATE SUCCESS").response()
        except ValueError as e:
            raise NewError(404, str(e))
        except Exception as e:
            logger.error("Can't update customer info", exc_info=e)
            raise NewError(500, str(e))