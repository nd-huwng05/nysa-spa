import uuid
from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from app.core.logger import logger
from app.core.errors import NewPackage, NewError
from ..repository.models import Invoice
from ..repository.repo import Repository
from ...service import ServiceConfig


class Service:
    def __init__(self, repo:Repository, config: ServiceConfig):
        self.repo = repo
        self.config = config

    def get_invoice_data(self, booking):
        sub_total = booking.total_amount

        discount_total = 0
        if booking.voucher_usage:
            discount_total = booking.voucher_usage.discount_amount

        total = sub_total - discount_total
        total_final = total + total*self.config.private_config.get("VAT")/100
        deposit = total_final*self.config.private_config.get("DEPOSIT_PERCENT")/100
        return {
            "total": total_final,
            "vat": self.config.private_config["VAT"],
            "vat_value": total*self.config.private_config.get("VAT")/100,
            "deposit_percent": self.config.private_config["DEPOSIT_PERCENT"],
            "deposit": deposit,
            "discount_total": discount_total,
        }


    def search_invoice(self, booking_id):
        try:
            invoice = self.repo.get_invoices_old(booking_id)
            if invoice:
                return invoice, None

            invoices_code = f"IV{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:4].upper()}"
            invoice_tmp = self.repo.create_invoice_tmp(invoices_code, booking_id)
            return invoice_tmp, None
        except IntegrityError as e:
            self.repo.db.session.rollback()
            return 500, "BOOKING NOT FOUND"

        except Exception as e:
            self.repo.db.session.rollback()
            logger.error("ERROR CREATING INVOICE", data=str(e))
            return 500, "INTERNAL SERVER ERROR"



    def update_invoice(self, invoices):
        try:
            invoice = self.repo.get_invoice_by_code(invoices.get("invoice_code"))
            if not invoice:
                raise NewError(400,"INVOICE NOT FOUND")

            invoice.payment_method = invoices.get("payment_method")
            invoice.payment_type = invoices.get("payment_type")
            invoice.type = invoices.get("type")
            invoice.amount = invoices.get("amount")
            invoice.expires_at = datetime.now() + timedelta(minutes=self.config.private_config.get("INVOICE_EXPIRATION_TIME"))
            self.repo.db.session.commit()
            return invoice
        except Exception as e:
            self.repo.db.session.rollback()
            print(e)
            raise NewError(500,"Error Server")

    def sepay_webhook(self, transaction_content, amount_received):
        self.repo.sepay_webhook(transaction_content, amount_received)
        self.repo.db.session.commit()

    def check_invoice_status(self, invoice_code):
        return self.repo.check_invoice_status(invoice_code)