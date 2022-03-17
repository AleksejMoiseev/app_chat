from composites.repositories import user_storage, message_storage, chat_storage, chat_member_storage
from application.dto import User, Message, Chat, ChatMember
from application.interfaces import ServiceInterface

from classic.app.dto import DTO


class ChatsChange(DTO):
    pk: int
    title: str = None
    descriptions: str = None


class MessageValidator(DTO):
    user_id: int
    chat_id: int
    body: str = ''


class UserService(ServiceInterface):
    def register(self, user: User):
        user = self._repository.add(user)
        return user

    def get_user(self, pk):
        user = self._repository.get(pk)
        return user

    def get_users(self, limit=None, offset=None, **params):
        users = self._repository.get_list(limit=limit, offset=offset, **params)
        return users


class MessageService(ServiceInterface):
    def send_message(self, message: Message):
        message = self._repository.add(message)
        return message

    def get_messages(self, limit=None, offset=None, **params):
        messages = self._repository.get_list(limit=limit, offset=offset, **params)
        return messages


class ChatService(ServiceInterface):
    def create_chat(self, chat: Chat):
        chat = self._repository.add(chat)
        return chat

    def delete_chat(self, pk):
        return self._repository.delete(pk)

    def update_chat(self, pk, params):
        pass

    def get_chat(self, pk):
        chat = self._repository.get(pk)
        return chat

    def get_chats(self, limit=None, offset=None, **params):
        chats = self._repository.get_list(limit=limit, offset=offset, **params)
        return chats


class ChatMemberService(ServiceInterface):
    def get_members(self, limit=None, offset=None, **params):
        members = self._repository.get_list(limit=limit, offset=offset, **params)
        return members

    def create_members(self, chat_member: ChatMember):
        chat_member = self._repository.add(chat_member)
        return chat_member


user_service = UserService(repository=user_storage)
message_service = MessageService(repository=message_storage)
chat_service = ChatService(repository=chat_storage)
chat_member_service = ChatMemberService(repository=chat_member_storage)
