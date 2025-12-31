import uuid
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from flask import Request

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
        code = request.args.get('code', None)
        if code is None:
            raise ValueError("'code' is required")

        booking = self.env.modules.booking_module.service.get_booking_by_code(code)
        if booking is None:
            raise ValueError("NO FOUND BOOKING")
        data = self.service.get_invoice_data(booking)

        return {
            'variable': data,
            'booking': booking,
            'booking_detail': booking.booking_details,
        }

    def handle_create_invoice(self, request: Request):
        invoice_code = f"IV{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:4].upper()}"
        voucher_code = request.form.get('voucher_code', None)
        booking_code = request.form.get('booking_code', None)
        if booking_code is None:
            raise ValueError("NO FOUND BOOKING")

        booking = self.env.modules.booking_module.service.get_booking_by_code(booking_code)
        if not booking:
            raise ValueError("BOOKING NOT FOUND")

        voucher_value = 0
        if voucher_code:
            voucher = self.env.modules.voucher_module.service.get_voucher_by_code(voucher_code)
            voucher_value = booking.total_amount*voucher.discount_value/100 if voucher.discount_value == "PERCENT" else voucher.discount_value

        payment_type = request.form.get('payment_type', None)
        if payment_type is None:
            raise ValueError("YOU NEED CHOOSE PAYMENT TYPE")

        amount = 0
        if payment_type == 'FULL':
            amount = booking.total_amount  - voucher_value + booking.total_amount*Decimal(self.config.private_config.get('VAT'))/100
        elif payment_type == 'DEPOSIT':
            amount = (booking.total_amount  - voucher_value + booking.total_amount*Decimal(self.config.private_config.get('VAT'))/100)*self.config.private_config.get('DEPOSIT_PERCENT')/100

        payment_methods = request.form.get('payment_method', None)
        if payment_methods is None:
            raise ValueError('YOU NEED CHOOSE PAYMENT METHOD')


        invoice = {
            'booking_id': booking.id,
            'invoice_code': invoice_code,
            'amount': amount,
            'payment_type': payment_type,
            'payment_method': payment_methods,
            'expires_at': datetime.now() + timedelta(minutes=self.config.private_config.get('INVOICE_EXPIRATION_TIME')) if payment_methods == "BANK_TRANSFER" else None,
        }

        invoice = self.service.create_invoice(invoice)

        if payment_methods == "BANK_TRANSFER":
            bank_id = self.config.private_config.get('BANK_ID')
            if bank_id is None:
                logger.error('BANK_ID not set')
                raise Exception('INTERNAL SERVER ERROR')

            account_no = self.config.private_config.get('ACCOUNT_NO')
            if account_no is None:
                logger.error('ACCOUNT_NO not set')
                raise Exception('INTERNAL SERVER ERROR')


            qr_link = f"https://qr.sepay.vn/img?acc={account_no}&bank={bank_id}&amount={int(invoice.amount)}&des={invoice.invoice_code}&template=compact"
            data = {
                'invoice': invoice,
                'qr_link':qr_link,
                'invoice_code':invoice.invoice_code,
                'expires_at': invoice.expires_at.strftime("%Y-%m-%d %H:%M:%S") if invoice.expires_at else None,
            }
            return data

        data = {
            'invoice': invoice,
            'invoice_code': invoice.invoice_code,
            'amount': Decimal(invoice.amount),
        }
        return data

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
            "status": invoice.status.value,
        }

        return NewPackage(data).response()

    def update_status(self, invoice_code):
        self.service.update_status(invoice_code)
        return NewPackage(message="PAYMENT SUCCESSFULLY").response()