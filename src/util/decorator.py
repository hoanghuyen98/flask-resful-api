from functools import wraps
from flask import request

from src.service.auth_service import AuthService


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = AuthService.get_logged_in_user(request)
        token = data.get('data')
        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated

