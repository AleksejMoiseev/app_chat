from classic.http_api import App
from pydantic import ValidationError

from application.user_application import services
from application.user_application.errors import BadRequest, handle
from .controllers import Users
from .middleware import JSONTranslator


def create_app(
    user_service: services.UserService,
) -> App:
    middleware = [
        JSONTranslator(),

    ]

    app = App(middleware=middleware, prefix='/api')
    app.register(Users(user_service=user_service))
    app.add_error_handler(ValidationError, handle)
    app.add_error_handler(BadRequest)
    return app