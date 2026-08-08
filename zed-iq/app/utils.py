from functools import wraps

from flask import abort
from flask_login import current_user


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = getattr(current_user, "role", None)
            if role == "admin":
                role = "super_admin"
            normalized = {"super_admin" if item == "admin" else item for item in roles}
            if not current_user.is_authenticated or role not in normalized:
                abort(403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def staff_required(fn):
    return role_required("super_admin", "teacher")(fn)
