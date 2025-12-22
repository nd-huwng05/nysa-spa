from flask import request, render_template, redirect, url_for, flash, session
from .handler import Handler

class Controller:
    def __init__(self, config, service, env):
        self.handler = Handler(config, service, env)

    def index(self):
        return render_template('page/admin.html')

    def dashboard(self):
        return render_template('components/dashboard.html')

    def voucher(self):
        return render_template('components/voucher.html')

    def settings(self):
        return render_template('components/setting.html')