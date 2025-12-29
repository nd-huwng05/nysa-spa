from functools import wraps
from flask import abort, request, redirect, url_for
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "ADMIN":
            return abort(403)
        return func(*args, **kwargs)

    return decorated_function


def staff_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        accepted_roles = ['STAFF', 'ADMIN']
        if not current_user.is_authenticated or current_user.role not in accepted_roles:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_function


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('user.login', callback=request.url))
        return func(*args, **kwargs)
    return decorated_function