from adapters.storage.storage import (
    UserPythonStructRepository, MessagePythonStructRepository,
    ChatMemberPythonStructRepository, ChatPythonStructRepository,
)
from application.services import UserService, MessageService, ChatService, ChatMemberService
from adapters.chat_api import app


user_storage = UserPythonStructRepository('users')
message_storage = MessagePythonStructRepository('message')
chat_storage = ChatPythonStructRepository('chat')
chat_member_storage = ChatMemberPythonStructRepository("chat_member")


user_service = UserService(repository=user_storage)
message_service = MessageService(messages_repo=message_storage)
chat_service = ChatService(chats_repo=chat_storage, members_repo=chat_member_storage)
chat_member_service = ChatMemberService(chat_member_repo=chat_member_storage)
