from flask import request, render_template, redirect, url_for, flash, session
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)


    def book_view(self):
        data ,error = self.handler.handler_book_view(request)
        if error:
            return redirect(url_for('service.service_search_view', message=str(error)))
        return render_template('page/book_view.html', **data)

    def staff_appointment(self):
        return self.handler.handler_staff_appointment(request)

    @staticmethod
    def book_confirm():
        return render_template('page/book_confirm.html')

