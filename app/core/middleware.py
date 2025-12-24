from functools import wraps
from flask import abort
from flask_jwt_extended import current_user


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
