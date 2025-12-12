from flask import request, render_template, redirect, url_for, flash, session
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)


    def book_view(self):
        data,error = self.handler.handler_book_view()

        if error:
            return redirect('/service/service-search')

        return render_template('page/book_view.html',**data)




    @staticmethod
    def book_confirm():
        return render_template('page/book_confirm.html')

