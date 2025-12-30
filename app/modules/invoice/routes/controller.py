from flask import request, render_template, redirect, url_for, flash, session

from app.core.errors import NewError
from app.core.logger import logger
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    def invoice_view(self):
        try:
            data = self.handler.get_data_for_view(request)
            return render_template('page/invoice.html', **data)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('home.index'))
        except Exception as e:
            logger.error('Error in invoice view', data=e)
            flash("INTERNAL SERVER ERROR", 'error')
            return redirect(url_for('home.index'))

    def invoice_create(self):
        try:
            data = self.handler.handle_create_invoice(request)
            qr_code = render_template("components/qrcode.html", **data)
            confirm = render_template("components/confirm.html", **data)
            return qr_code + confirm
        except ValueError as e:
            flash(str(e), 'error')
            return "", 400
        except Exception as e:
            flash("INTERNAL SERVER ERROR", 'error')
            logger.error('Error in invoice view', data=e)
            return "", 500

    def sepay_webhook(self):
        return self.handler.sepay_webhook(request)

    def check_status(self, invoice_code):
        return self.handler.check_status(invoice_code)

    def staff_view(self):
        return render_template('components/staff_invoice.html')

    def update_status(self, invoice_code):
        try:
            self.handler.update_status(invoice_code)
        except ValueError as e:
            flash(str(e), 'error')
            return NewError(message=str(e), status_code=400)
        except Exception as e:
            flash("INTERNAL SERVER ERROR", 'error')
            logger.error('Error in invoice view', data=e)
            return NewError(message="INTERNAL SERVER ERROR", status_code=500)