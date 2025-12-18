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


