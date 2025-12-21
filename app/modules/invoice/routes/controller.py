from flask import request, render_template, redirect, url_for, flash, session
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    def invoice_view(self):
        data, errors = self.handler.get_data_for_view(request)
        if errors:
            flash(errors, category='error')
            return redirect(url_for('home.index'))

        return render_template('page/invoice.html', **data)

    def update_invoice(self):
       return self.handler.handle_update_invoice(request)

    def sepay_webhook(self):
        return self.handler.sepay_webhook(request)

    def check_status(self, invoice_code):
        return self.handler.check_status(invoice_code)

    def staff_view(self):
        return render_template('components/staff_invoice.html')