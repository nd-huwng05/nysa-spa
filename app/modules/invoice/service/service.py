import uuid
from datetime import datetime
from app.core.errors import NewPackage, NewError
from ..repository.models import Invoice
from ..repository.repo import Repository
from ...service import ServiceConfig


class Service:
    def __init__(self, repo:Repository, config: ServiceConfig):
        self.repo = repo
        self.config = config

    def get_invoice_data(self,booking):
        code = f"IV{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:4].upper()}"
        sub_total = booking.total_amount

        discount_total = 0
        if booking.voucher_usage:
            discount_total = booking.voucher_usage.discount_amount

        total = sub_total - discount_total
        total_final = total + total*self.config.private_config.get("VAT")/100
        deposit = total*self.config.private_config.get("DEPOSIT_PERCENT")/100
        return {
            "code": code,
            "total": total_final,
            "vat": self.config.private_config["VAT"],
            "vat_value": total*self.config.private_config.get("VAT")/100,
            "deposit_percent": self.config.private_config["DEPOSIT_PERCENT"],
            "deposit": deposit,
            "discount_total": discount_total,
        }

    def create_invoice(self, invoice):
        try:
            old_invoice = self.repo.get_invoice_by_booking_id(invoice.get("booking_id"))
            if old_invoice:
                old_invoice.payment_method = invoice.get("payment_method")
                old_invoice.payment_type = invoice.get("payment_type")
                old_invoice.amount = invoice.get("amount")
                self.repo.db.session.commit()
                return old_invoice
            else:
                new_invoice = Invoice(
                    invoice_code=invoice.get("invoice_code"),
                    booking_id=invoice.get("booking_id"),
                    type=invoice.get("type"),
                    amount=invoice.get("amount"),
                    payment_method=invoice.get("payment_method"),
                    payment_type=invoice.get("payment_type"),
                )
                self.repo.create_new_invoice(new_invoice)
                self.repo.db.session.commit()
                return new_invoice
        except Exception as e:
            self.repo.db.session.rollback()
            print(e)
            raise NewError(500,"Error Server")

    def sepay_webhook(self, transaction_content, amount_received):
        self.repo.sepay_webhook(transaction_content, amount_received)
        self.repo.db.session.commit()

    def check_invoice_status(self, invoice_code):
        return self.repo.check_invoice_status(invoice_code)