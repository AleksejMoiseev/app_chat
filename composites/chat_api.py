from classic.aspects import points
from classic.messaging_kombu import KombuPublisher
from classic.sql_storage import TransactionContext
from gevent import monkey, pywsgi
from kombu import Connection
from sqlalchemy import create_engine

from adapters import database
from adapters import message_bus
from adapters.chat_api import app
from adapters.database.settings import CONF
from adapters.database.sqlstorage import (
    UserRepository, MessageRepository, ChatRepository, ChatMemberRepository
)
from application.dataclases import User, Message, Chat, ChatMember
from application.services import UserService, MessageService, ChatService, ChatMemberService

monkey.patch_all()

engine = create_engine(database.settings.DB_URL, echo=True)

database.metadata.create_all(engine)

transaction_ctx = TransactionContext(bind=engine, expire_on_commit=False)


user_storage = UserRepository(model=User, default_limit=CONF.default_limit.value, context=transaction_ctx)
message_storage = MessageRepository(model=Message, default_limit=CONF.default_limit.value, context=transaction_ctx)
chat_storage = ChatRepository(model=Chat, default_limit=CONF.default_limit.value, context=transaction_ctx)
chat_member_storage = ChatMemberRepository(
    model=ChatMember, default_limit=CONF.default_limit.value, context=transaction_ctx
)


class MessageBus:
    settings = message_bus.settings
    connection = Connection(settings.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


user_service = UserService(repository=user_storage)
message_service = MessageService(messages_repo=message_storage, publisher=MessageBus.publisher)
chat_service = ChatService(chats_repo=chat_storage, members_repo=chat_member_storage)
chat_member_service = ChatMemberService(chat_member_repo=chat_member_storage)


class Aspects:
    points.join(MessageBus.publisher, transaction_ctx)


app = app.create_app(
    chat_service=chat_service,
    message_service=message_service,
    chat_member_service=chat_member_service,
    user_service=user_service
)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(("localhost", 8080), app)  # address and port to bind, and the Falcon handler API
    server.serve_forever()  # once the server is created, let it serve forever
