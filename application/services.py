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


class ChatInteractor:
    def __init__(self, chat_member, chat, message, user_service):
        self.chat_member = chat_member
        self.chat = chat
        self.message = message
        self.user = user_service

    def create_chat(self, chat):
        chat = self.chat.create_chat(chat)
        params = {
            "user_id": chat.owner,
            "chat_id": chat.pk,
        }
        chat_member = ChatMember(**params)
        self.chat_member.create_members(chat_member)
        return chat

    def delete_chat(self, chat_id):
        members = self.chat_member.get_members()
        for member in members:
            if member.chat_id == chat_id:
                member.kicked = datetime.now()
        return self.chat.delete_chat(chat_id)

    def send_message(self, message):
        return self.message.send_message(message)

    def get_messages_by_chat_id(self, user_id, chat_id, limit, offset):
        messages = self.message.get_messages(limit=limit, offset=offset)
        messages_body = []
        for message in messages:
            if message.chat_id == chat_id:
                messages_body.append(message)
        return messages_body

    def get_members_by_chat(self, chat_id):
        members_all = self.chat_member.get_members()
        members = []
        for member in members_all:
            if member.chat_id == chat_id and not member.kicked:
                members.append(member)
        return members

    def get_user(self, pk):
        return self.user.get_user(pk)

    def add_member_to_chat(self, member: ChatMember):
        return self.chat_member.create_members(member)

    def get_chat(self, chat_id):
        return self.chat.get_chat(chat_id)

    def get_chats(self):
        return self.chat.get_chats()

    def get_members(self):
        return self.chat_member.get_members()

    def get_member(self, user_id):
        member = self.chat_member.get_member(user_id)
        if not member:
            raise ValueError('Member not found')
        return member

    def delete_member(self, user_id, chat_id):
        members = self.get_members_by_chat(chat_id)
        for member in members:
            if member.user_id == user_id:
                member.kicked = datetime.now()
                return self.chat_member.delete_member(user_id)
        return None

    @staticmethod
    def is_owner(owner, chat):
        if owner.pk == chat.owner:
            return True
        return False

    def is_member(self, user_id, chat_id):
        members_by_chat = self.get_members_by_chat(chat_id)
        for member in members_by_chat:
            if user_id == member.user_id:
                return True
        return False
