from functools import wraps
from flask import redirect
from flask_login import current_user

def is_user(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        user = current_user
        if user.role_id != 1:
            return redirect('/')
        return function(*args, **kwargs)
    return decorated_function


def is_admin(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        user = current_user
        if user.role_id != 2:
            return redirect('/')
        return function(*args, **kwargs)
    return decorated_function