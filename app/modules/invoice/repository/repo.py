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

    @staticmethod
    def get_invoice_by_code(code):
        return Invoice.query.filter(Invoice.invoice_code == code).first()

    @staticmethod
    def sepay_webhook(transaction_content, amount_received):
        invoice = Invoice.query.filter(Invoice.status == 'PENDING',
                                      amount_received >= Invoice.amount,
                                      func.lower(transaction_content).contains(func.lower(Invoice.invoice_code))
                                      ).first()
        if invoice:
            invoice.status = InvoiceStatus.PAID.value
            invoice.booking.status = "SUCCESS"
            invoice.booking.payment = "PARTIAL" if invoice.payment_type == "DEPOSIT" else "COMPLETE"

    @staticmethod
    def check_invoice_status(invoice_code):
        return Invoice.query.filter(Invoice.invoice_code == invoice_code).first()

    @staticmethod
    def get_invoices_old(booking_id):
        return Invoice.query.filter(Invoice.booking_id == booking_id,
                                    Invoice.status == InvoiceStatus.PENDING.value).first()

    def create_invoice_tmp(self, invoice_code, booking_id):
        new_invoice = Invoice(booking_id=booking_id,
                              invoice_code=invoice_code)
        self.db.session.add(new_invoice)
        self.db.session.commit()
        return new_invoice