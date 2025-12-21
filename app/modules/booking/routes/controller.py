from flask import request, render_template, redirect, url_for, flash, session

from app.core.errors import NewPackage
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
        staff_appointment = self.handler.handler_staff_appointment(request)
        staff_list = staff_appointment.get('staff_appointment', [])
        return render_template('components/staff_dropdown.html', staffs=staff_list)

    def staff_appointment_json(self):
        staff_appointment = self.handler.handler_staff_appointment(request)
        staff_list = staff_appointment.get('staff_appointment', [])
        return NewPackage(staff_list).response()


    def booking_voucher(self):
        vouchers = self.handler.handler_booking_voucher(request)
        return render_template('components/vouchers.html', vouchers=vouchers)

    def add_booking(self):
        return self.handler.handler_add_booking(request)

    def staff_booking(self):
        data = self.handler.get_data_for_staff_booking(request)
        return render_template('components/tab_booking.html', **data)

    def staff_booking_details(self):
        data = self.handler.get_data_for_staff_booking_details(request)
        return render_template('components/booking_details.html',  **data)