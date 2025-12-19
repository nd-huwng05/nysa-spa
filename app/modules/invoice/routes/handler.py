import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Request, g, jsonify

from app.core.logger import logger
from app.core.errors import NewError, NewPackage
from ..config.config_module import InvoiceConfig
from ..service.service import Service

class Handler:
    def __init__(self, config: InvoiceConfig, service:Service, env):
        self.config = config
        self.service = service
        self.env = env

    def get_data_for_view(self, request: Request):
        booking_id = request.args.get('booking_id', None)

        if booking_id is None:
            return None, 'BOOKING_ID is required'
        booking = self.env.modules.booking_module.service.get_booking_by_id(booking_id)

        if booking is None:
            return None, 'NOT FOUND BOOKING'

        if booking.status.value != 'PENDING':
            return None, 'Booking is paid or awaiting payment or cancelled'

        invoice_data = self.service.get_invoice_data(booking)

        return {
            'variable': invoice_data,
            'booking': booking,
            'booking_detail': booking.booking_details,
        }, None

    def handle_create_invoice(self, request: Request):
        data = request.json

        booking_id = data.get('booking_id', None)

        if booking_id is None:
            raise NewError(400,'BOOKING_ID is required')

        invoice_code = data.get('invoice_code', None)
        if invoice_code is None:
            raise NewError(400,'INVOICE_CODE is required')

        amount = data.get('amount', None)
        if amount is None:
            raise NewError(400,'AMOUNT is required')

        payment_type = data.get('payment_type', None)
        if payment_type is None:
            raise NewError(400,'PAYMENT_TYPE is required')

        payment_methods = data.get('payment_method', None)
        if payment_methods is None:
            raise NewError(400,'PAYMENT_METHODS is required')

        type = data.get('type', None)
        if type is None:
            raise NewError(400,'TYPE is required')

        invoice = {
            'invoice_code': invoice_code,
            'booking_id': booking_id,
            'amount': amount,
            'payment_type': payment_type,
            'payment_method': payment_methods,
            'type': type,
        }

        invoice = self.service.create_invoice(invoice)

        if payment_type == 'DEPOSIT':
            self.env.modules.booking_module.service.update_payment_booking(booking_id, 'PARTIAL')

        if payment_type == 'FULL':
            self.env.modules.booking_module.service.update_payment_booking(booking_id, 'COMPLETE')


        if payment_methods == "BANK_TRANSFER":
            bank_id = self.config.private_config.get('BANK_ID')
            if bank_id is None:
                logger.error('BANK_ID not set')
                raise NewError(500, 'Server Error')

            account_no = self.config.private_config.get('ACCOUNT_NO')
            if account_no is None:
                logger.error('ACCOUNT_NO not set')
                raise NewError(500, 'Server Error')


            qr_link = f"https://qr.sepay.vn/img?acc={account_no}&bank={bank_id}&amount={int(invoice.amount)}&des={invoice.invoice_code}&template=compact"
            data = {
                'qr_link':qr_link,
                'invoice_code':invoice.invoice_code,
            }
            return NewPackage(data).response()

        data = {
            'invoice_code': invoice.invoice_code,
        }
        return NewPackage(data).response()

    def sepay_webhook(self, request: Request):
        data = request.json
        if not data:
            raise NewError(400, 'NO DATA RECEIVED')
        transaction_content = data.get('content', None)
        raw_amount = data.get('transferAmount', 0)

        try:
            amount_received = Decimal(str(raw_amount))
        except (InvalidOperation, ValueError):
            raise NewError(400, 'INVALID_AMOUNT_FORMAT')

        self.service.sepay_webhook(transaction_content, amount_received)
        return NewPackage(message="PAYMENT SUCCESSFULLY").response()

    def check_status(self, invoice_code):
        invoice = self.service.check_invoice_status(invoice_code)
        if not invoice:
            raise NewError(400, 'INVOICE_CODE NOT FOUND')

        data = {
            "invoice_code": invoice.invoice_code,
            "status": invoice.status.value
        }

        return NewPackage(data).response()

