from classic.http_api import App

from .middleware import JSONTranslator
from application.user_application import services
from .controllers import Users


def create_app(
    user_service: services.UserService,
) -> App:
    middleware = [
        JSONTranslator(),

    ]

    app = App(middleware=middleware, prefix='/api')
    app.register(Users(user_service=user_service))

    return app