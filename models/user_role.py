from functools import wraps
from flask import abort
from flask_login import current_user


class Role:
    ADMIN = 'admin'
    USER = 'user'
    MANAGER = 'manager'


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)  # Chyba 403: Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator
