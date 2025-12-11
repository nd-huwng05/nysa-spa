from flask import redirect, url_for, request, session
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTExtendedException
from functools import wraps

def jwt_middleware(view_fun):
    @wraps(view_fun)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(locations=['cookies'])
            return view_fun(*args, **kwargs)
        except (NoAuthorizationError, JWTExtendedException):
            return redirect(url_for('user.login', callback_url=request.full_path))
    return wrapper