from app.core.errors import NewError, NewPackage
from ..service.service import Service

class Handler:
    def __init__(self, config, service:Service, env):
        self.config = config
        self.service = service
        self.env = env

    def voucher_suitable(self, request):
        customer_id = request.args.get('customer')
        if customer_id is None:
            return NewError(400, 'CUSTOMER IS REQUIRED')

        price = request.args.get('price')
        if price is None:
            return NewError(400, 'PRICE IS REQUIRED')

        voucher = self.service.get_list_voucher_customer(customer_id, price)
        voucher = [v.to_json() for v in voucher]
        return NewPackage(voucher).response()

