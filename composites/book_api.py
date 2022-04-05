from classic.aspects import points
from classic.sql_storage import TransactionContext
from gevent import monkey, pywsgi
from kombu import Connection
from sqlalchemy import create_engine
from classic.messaging_kombu import KombuPublisher
from adapters.book_api import app
from adapters.database import bookdb
from adapters.database.bookdb.settings import CONF
from adapters.database.bookdb.storage import BookRepository
from application.book_aplication.dataclases import Book
from application.book_aplication.services import BookService
from adapters import message_bus

monkey.patch_all()

engine = create_engine(bookdb.settings.DB_URL, echo=True)

bookdb.metadata.create_all(engine)

transaction_ctx = TransactionContext(bind=engine, expire_on_commit=False)


book_storage = BookRepository(model=Book, default_limit=CONF.default_limit.value, context=transaction_ctx)


class MessageBus:
    settings = message_bus.settings
    connection = Connection(settings.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


book_service = BookService(repository=book_storage, publisher=MessageBus.publisher)


class Aspects:
    points.join(MessageBus.publisher, transaction_ctx)


app = app.create_app(
    service=book_service
)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(("localhost", 8080), app)  # address and port to bind, and the Falcon handler API
    server.serve_forever()  # once the server is created, let it serve forever
