import flask
from flask import render_template, request, redirect, url_for
from flask_jwt_extended import create_access_token

from app.user.service import Service

def login():
    if request.method == 'GET':
        return render_template('page/login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    user = Service.authenticate(username, password)

    if not user:
        flask('Username or Password incorrect','danger')
        return redirect(url_for('user.login'))

    access_token = create_access_token()

def logout():
    pass

def register():
    pass

def refresh():
    pass

def dashboard():
    pass