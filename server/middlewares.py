from functools import wraps

######################################################
#              Middlewares declaration               #
######################################################
from http import HTTPStatus

from flask import request

from secrets import Secrets
from server.interfaces.ApiResponse import ApiResponse


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return ApiResponse("Not authorized", None, ["Token is missing"], HTTPStatus.FORBIDDEN).build()

        if token == Secrets.API_TOKEN:
            return ApiResponse("Not authorized", None, ["Token is invalid"], HTTPStatus.FORBIDDEN).build()

        return f(*args, **kwargs)

    return decorator
