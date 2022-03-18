from datetime import datetime

from classic.app.dto import DTO

from application.dto import User, Message, Chat, ChatMember


class ChatsChange(DTO):
    pk: int
    title: str = None
    descriptions: str = None


class MessageValidator(DTO):
    user_id: int
    chat_id: int
    body: str = None


class ChatMemberValidator(DTO):
    user_id: int
    chat_id: int
    checked_out: datetime = None
    kicked: datetime = None


class UserService:

    def __init__(self, repository):
        self._repository = repository

    def register(self, user: User):
        user = self._repository.add(user)
        return user

    def get_user(self, pk):
        user = self._repository.get(pk)
        return user

    def get_users(self, limit=None, offset=None, **params):
        users = self._repository.get_list(limit=limit, offset=offset, **params)
        return users


class MessageService:
    def __init__(self, repository):
        self._repository = repository

    def send_message(self, message: Message):
        message = self._repository.add(message)
        return message

    def get_messages(self, limit=None, offset=None, **params):
        messages = self._repository.get_list(limit=limit, offset=offset, **params)
        return messages


class ChatService:
    def __init__(self, repository):
        self._repository = repository

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


class ChatMemberService:

    def __init__(self, repository):
        self._repository = repository

    def get_members(self, limit=None, offset=None, **params):
        members = self._repository.get_list(limit=limit, offset=offset, **params)
        return members

    def create_members(self, chat_member: ChatMember):
        chat_member = self._repository.add(chat_member)
        return chat_member

    def get_member(self, pk):
        return self._repository.get(pk)

    def delete_member(self, pk):
        chat_member = self._repository.delete(pk)
        return chat_member
