from classic.aspects import points
from classic.sql_storage import TransactionContext
from gevent import monkey, pywsgi
from sqlalchemy import create_engine

from adapters.database import bookdb
from adapters.database.bookdb.settings import CONF
from adapters.database.bookdb.storage import BookRepository
from adapters.book_api import app
from application.book_aplication.dataclases import Book
from application.book_aplication.services import BookService

monkey.patch_all()

engine = create_engine(bookdb.settings.DB_URL, echo=True)

bookdb.metadata.create_all(engine)

transaction_ctx = TransactionContext(bind=engine, expire_on_commit=False)


book_storage = BookRepository(model=Book, default_limit=CONF.default_limit.value, context=transaction_ctx)

book_service = BookService(repository=book_storage)


points.join(transaction_ctx)

app = app.create_app(
    service=book_service
)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(("localhost", 8080), app)  # address and port to bind, and the Falcon handler API
    server.serve_forever()  # once the server is created, let it serve forever
