from sqlalchemy import func

from .models import Invoice, InvoiceStatus, InvoiceType


class Repository:
    def __init__(self, env):
        self.env = env
        self.db = self.env.db

    @staticmethod
    def get_invoice_by_booking_id(booking_id:int):
        invoice = Invoice.query.filter(
            Invoice.booking_id == booking_id,
            Invoice.type == 'PAYMENT',
            Invoice.status == 'PENDING',
        ).first()
        return invoice

    def create_new_invoice(self, new_invoice):
        new_invoice.status = InvoiceStatus.PENDING
        self.db.session.add(new_invoice)

    def sepay_webhook(self, transaction_content, amount_received):
        invoice = Invoice.query.filter(Invoice.status == 'PENDING',
                                      amount_received >= Invoice.amount,
                                      func.lower(transaction_content).contains(func.lower(Invoice.invoice_code))
                                      ).first()
        if invoice:
            invoice.status = InvoiceStatus.PAID.value

    @staticmethod
    def check_invoice_status(invoice_code):
        return Invoice.query.filter(Invoice.invoice_code == invoice_code).first()