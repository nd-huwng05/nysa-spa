import typing as t
from wsgiref.types import WSGIEnvironment

from flask import jsonify
from werkzeug import Request as WSGIRequest
from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response


class NewError(HTTPException):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.description = message
        super(NewError, self).__init__(description=message)

    def get_response(
        self,
        environ: WSGIEnvironment | WSGIRequest | None = None,
        scope: dict[str, t.Any] | None = None,
    ) -> Response:
        response = jsonify({
            'status': 'error',
            'code': self.status_code,
            'message': self.description,
        })
        response.status_code = self.status_code
        return response

class NewPackage:
    def __init__(self, data=None, message="Success", status_code=200):
        self.data = data
        self.message = message
        self.status_code = status_code

    def response(self)-> Response:
        response = jsonify({
            'status': 'success',
            'code': self.status_code,
            'message': self.message,
            'data': self.data,
        })
        response.status_code = self.status_code
        return response
