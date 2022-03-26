from gevent import monkey, pywsgi

from adapters.chat_api import app
from adapters.storage.storage import (
    UserPythonStructRepository, MessagePythonStructRepository,
    ChatMemberPythonStructRepository, ChatPythonStructRepository,
)
from application.services import UserService, MessageService, ChatService, ChatMemberService

monkey.patch_all()

user_storage = UserPythonStructRepository('users')
message_storage = MessagePythonStructRepository('message')
chat_storage = ChatPythonStructRepository('chat')
chat_member_storage = ChatMemberPythonStructRepository("chat_member")


user_service = UserService(repository=user_storage)
message_service = MessageService(messages_repo=message_storage)
chat_service = ChatService(chats_repo=chat_storage, members_repo=chat_member_storage)
chat_member_service = ChatMemberService(chat_member_repo=chat_member_storage)


app = app.create_app(
    chat_service=chat_service,
    message_service=message_service,
    chat_member_service=chat_member_service,
    user_service=user_service
)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(("localhost", 8080), app)  # address and port to bind, and the Falcon handler API
    server.serve_forever()  # once the server is created, let it serve forever
