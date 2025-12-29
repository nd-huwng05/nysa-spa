from flask import request, render_template, flash, url_for, redirect, make_response
from app.core.logger import logger
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    def book_view(self):
        try:
            data = self.handler.get_data_for_booking(request)
            return render_template('page/book_view.html', **data)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('service.service_search_view'))
        except Exception as e:
            logger.error(msg="Throw at book_view", data=str(e))
            flash("INTERNAL SERVER ERROR", 'error')
            return redirect(url_for('service.service_search_view'))

    def staff_appointment(self):
        try:
            data = self.handler.get_appointment_staff(request)
            step_two = render_template('components/step_two.html', **data)
            summary = render_template('components/summary.html', **data)
            return step_two + summary
        except ValueError as e:
            flash(str(e), 'error')
            return "", 204
        except Exception as e:
            logger.error(msg="Throw at staff_appointment", data=str(e))
            flash("INTERNAL SERVER ERROR", 'error')
            return "", 204

    def booking_create(self):
        try:
            self.handler.handler_create_booking(request)
            flash("BOOKING CREATED", 'success')
            response = make_response("", 200)
            response.headers["HX-Redirect"] = url_for('invoice.invoice_view')
            return response
        except ValueError as e:
            flash(str(e), 'error')
            return "", 400
        except Exception as e:
            logger.error(msg="Throw at booking_create", data=str(e))
            flash("INTERNAL SERVER ERROR", 'error')
            return "", 500