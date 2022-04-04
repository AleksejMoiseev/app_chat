from classic.http_api import App
from pydantic import ValidationError

from application.issue_aplication import services
from application.issue_aplication.errors import handle, BadRequest
from .controllers import IssueUsers
from .middleware import JSONTranslator


def create_app(
    service: services.IssueUserService,
) -> App:
    middleware = [
        JSONTranslator(),

    ]

    app = App(middleware=middleware, prefix='/api')
    app.register(IssueUsers(service=service))
    app.add_error_handler(ValidationError, handle)
    app.add_error_handler(BadRequest)
    return app