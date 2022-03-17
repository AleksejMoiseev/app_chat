import falcon
from classic.app.errors import AppError


class BadRequest(Exception):
    @staticmethod
    def handle(req, resp, exc, params):
        resp.set_header("X-Custom-Header", "*")
        resp.body = f"Parameters in a request cannot be validated"
        resp.status = falcon.HTTP_404


class UserNotFound(AppError):
    msg_template = "UserNotFound"
    code = 'UserNotFound'


class ParamsIsNotValid(AppError):
    msg_template = "ParamsIsNotValid"
    code = 'ParamsIsNotValid'