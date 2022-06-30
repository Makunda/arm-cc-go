from http import HTTPStatus
from typing import List

from flask import Response, make_response, jsonify

from server.errors.BadResponseDataError import BadResponseDataError
from utils.SerializableUtils import SerializableUtils


class ApiResponse:
    """
    Response returned by the server
    """

    message: str
    data: any
    errors: List[str]
    code: int

    def __init__(self, message: str, data: any = None, errors: List[str] = None, code: HTTPStatus = None):
        """
        Initialize an API response
        :param message: Message to pass to the API
        :param data: Data of the API response
        :param errors: List of error. If the list of error is not empty. An error code will be returned
        """
        # Verify inputs
        if errors is None:
            errors = []

        # Verify message
        if not SerializableUtils.is_jsonable(message):
            raise BadResponseDataError("message", "This field cannot be serialized")

        # Verify data
        if not SerializableUtils.is_jsonable(data):
            raise BadResponseDataError("data", "This field cannot be serialized")

        # Verify errors
        if not SerializableUtils.is_jsonable(errors):
            raise BadResponseDataError("errors", "This field cannot be serialized")

        # Verify the parameters can be serialized
        self.message = message
        self.data = data
        self.errors = errors

        # Apply code
        if code is not None:
            self.code = int(code.value)
        elif len(self.errors) == 0:
            self.code = HTTPStatus.OK
        else:
            # By default fallback on internal error
            self.code = HTTPStatus.BAD_REQUEST

    def build(self):
        """
        Build and return a response entity
        :return: The response entity
        """
        return make_response(jsonify({
            'message': self.message,
            'data': self.data,
            'errors': self.errors
            }),
            self.code
        )
