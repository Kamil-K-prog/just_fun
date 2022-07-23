from typing import Callable
from functools import wraps

from flask import redirect
from flask_login import current_user


def is_user(function: Callable) -> Callable:
    ("""Допускает к роуту только обычного пользователя. """
     """ВНИМАНИЕ: использовать только в тандеме с декоратором """
     """flask_login.login_required""")

    @wraps(function)
    def decorated_function(*args, **kwargs):
        user = current_user
        if user.role_id != 1:
            return redirect('/')
        return function(*args, **kwargs)
    return decorated_function


def is_admin(function: Callable) -> Callable:
    ("""Допускает к роуту только админа. """
     """ВНИМАНИЕ: использовать только в тандеме с декоратором """
     """flask_login.login_required""")

    @wraps(function)
    def decorated_function(*args, **kwargs):
        user = current_user
        if user.role_id != 2:
            return redirect('/')
        return function(*args, **kwargs)
    return decorated_function
