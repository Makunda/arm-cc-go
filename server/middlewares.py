from functools import wraps
######################################################
#              Middlewares declaration               #
######################################################
from http import HTTPStatus

from flask import request

from logger.Logger import Logger
from secrets import Secrets
from secrets.Secrets import IS_DEV
from server.interfaces.ApiResponse import ApiResponse

__logger = Logger.get("Middleware")


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # If development mode, by pass the authentication
        if IS_DEV:
            __logger.info(f"Auth route triggered in dev mode: {request.endpoint}")
            return f(*args, **kwargs)

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return ApiResponse("Not authorized", None, ["Token is missing"], HTTPStatus.FORBIDDEN).build()

        if token == Secrets.API_TOKEN:
            return ApiResponse("Not authorized", None, ["Token is invalid"], HTTPStatus.FORBIDDEN).build()

        return f(*args, **kwargs)

    return decorator
