from flask import request, render_template, redirect, url_for, flash, session
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    @staticmethod
    def book_view():
        return render_template('page/book_view.html')

    @staticmethod
    def book_confirm():
        return render_template('page/book_confirm.html')