from adapters.storage import PythonStructRepository
from application.services import UserService, MessageService, ChatService, ChatMemberService

user_storage = PythonStructRepository('users')
message_storage = PythonStructRepository('message')
chat_storage = PythonStructRepository('chat')
chat_member_storage = PythonStructRepository("chat_member")


user_service = UserService(repository=user_storage)
message_service = MessageService(repository=message_storage)
chat_service = ChatService(repository=chat_storage)
chat_member_service = ChatMemberService(repository=chat_member_storage)