from application.services import UserService, MessageService, ChatService, ChatMemberService
from composites.repositories import user_storage, message_storage, chat_storage, chat_member_storage

user_service = UserService(repository=user_storage)
message_service = MessageService(repository=message_storage)
chat_service = ChatService(repository=chat_storage)
chat_member_service = ChatMemberService(repository=chat_member_storage)