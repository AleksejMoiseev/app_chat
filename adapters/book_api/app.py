from classic.http_api import App
from pydantic import ValidationError

from application.book_aplication import services
from application.book_aplication.errors import handle, BadRequest
from .controllers import Books
from .middleware import JSONTranslator


def create_app(
    service: services.BookService,
) -> App:
    middleware = [
        JSONTranslator(),

    ]

    app = App(middleware=middleware, prefix='/api')
    app.register(Books(service=service))
    app.add_error_handler(ValidationError, handle)
    app.add_error_handler(BadRequest)
    return app