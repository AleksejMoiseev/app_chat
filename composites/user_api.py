from classic.aspects import points
from classic.messaging_kombu import KombuPublisher
from classic.sql_storage import TransactionContext
from gevent import monkey, pywsgi
from kombu import Connection
from sqlalchemy import create_engine

from adapters import message_bus
from adapters.database import userdb
from adapters.database.userdb.settings import CONF
from adapters.database.userdb.storage import UserRepository
from adapters.user_api import app
from application.user_application.dataclases import User
from application.user_application.services import UserService

monkey.patch_all()

engine = create_engine(userdb.settings.DB_URL, echo=True)

userdb.metadata.create_all(engine)

transaction_ctx = TransactionContext(bind=engine, expire_on_commit=False)


user_storage = UserRepository(model=User, default_limit=CONF.default_limit.value, context=transaction_ctx)


class MessageBus:
    settings = message_bus.settings
    connection = Connection(settings.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


user_service = UserService(repository=user_storage, publisher=MessageBus.publisher)


class Aspects:
    points.join(MessageBus.publisher, transaction_ctx)


app = app.create_app(
    user_service=user_service
)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(("localhost", 8080), app)  # address and port to bind, and the Falcon handler API
    server.serve_forever()  # once the server is created, let it serve forever
