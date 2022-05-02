from datetime import datetime

from classic.app.dto import DTO
from classic.components.component import component
from sqlalchemy.exc import InvalidRequestError
from classic.messaging import Publisher, Message
from adapters.message_bus.settings import ExchangeTopic

from application.dataclases import Chat, User, ChatMember, Message
from application.errors import BadRequest
from application.interfaces import (
    UserRepositoryInterface, MessageRepositoryInterface, ChatMembersRepositoryInterface,
    ChatRepositoryInterface,
)


class ChatsChange(DTO):
    id: int
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


@component
class UserService:
    _repository: UserRepositoryInterface

    def register(self, user: User):
        user = self._repository.add(user)
        return user

    def get_user(self, pk):
        user = self._repository.get(pk)
        return user

    def get_users(self, limit=None, offset=None, **params):
        users = self._repository.get_list(limit=limit, offset=offset, **params)
        return users

    def filer_by(self, params):
        try:
            entity_model = self._repository.filer_by(params)
        except (InvalidRequestError, ):
            raise BadRequest()
        return entity_model


@component
class MessageService:
    messages_repo: MessageRepositoryInterface
    #publisher: Publisher

    def _send_message(self, message: str):
        self.publisher.plan(
            Message(ExchangeTopic.exchange.value, {'message': message})
        )

    def send_message(self, message: Message):
        message = self.messages_repo.add(message)
        return message

    def get_messages(self, limit=None, offset=None, **params):
        messages = self.messages_repo.get_list(limit=limit, offset=offset, **params)
        return messages

    def get_messages_by_chat_id(self, user_id, chat_id, limit, offset):
        chats_messages = self.get_messages(limit=limit, offset=offset)
        messages = []
        for message in chats_messages:
            if message.chat_id == chat_id:
                messages.append(message)
        return messages


@component
class ChatService:
    chats_repo: ChatRepositoryInterface
    members_repo: ChatMembersRepositoryInterface

    def register_chat(self, chat: Chat):
        chat = self.chats_repo.add(chat)
        return chat

    def update_chat(self, chat_id, params):
        return self.chats_repo.update(chat_id, params)

    def _create_chat(self, chat: Chat):
        chat = self.register_chat(chat)
        params = {
            "user": chat.user,
            "chat": chat,
        }
        chat_member = ChatMember(**params)
        self.members_repo.add(chat_member)
        return chat

    def create_chat(self, user_id, data):
        chat = Chat(user=user_id, **data)
        return self._create_chat(chat)

    def _delete_chat(self, pk):
        return self.chats_repo.delete(pk)

    def delete_chat(self, chat_id):
        members = self.members_repo.get_list()
        for member in members:
            if member.chat_id == chat_id:
                member.kicked = datetime.now()
        return self._delete_chat(chat_id)

    def get_chat(self, pk):
        chat = self.chats_repo.get(pk)
        return chat

    def get_chat_by_owner(self, owner, chat_id):
        chat = self.get_chat(chat_id)
        if not chat:
            raise BadRequest()
        if owner != chat.user:
            raise BadRequest()
        return chat

    def get_chats(self, limit=None, offset=None, **params):
        chats = self.chats_repo.get_list(limit=limit, offset=offset, **params)
        return chats


@component
class ChatMemberService:
    chat_member_repo: ChatMembersRepositoryInterface

    def get_members(self, limit=None, offset=None, **params):
        members = self.chat_member_repo.get_list(limit=limit, offset=offset, **params)
        return members

    def create_members(self, chat_member: ChatMember):
        chat_member = self.chat_member_repo.add(chat_member)
        return chat_member

    def _get_member(self, pk):
        return self.chat_member_repo.get(pk)

    def _delete_member(self, pk):
        chat_member = self.chat_member_repo.delete(pk)
        return chat_member

    def get_members_by_chat(self, chat):
        return self.chat_member_repo.get_members_by_chat(chat)

    def get_member(self, user_id):
        member = self._get_member(user_id)
        if not member:
            raise ValueError('Member not found')
        return member

    def delete_member(self, user_id, chat_id):
        members = self.get_members_by_chat(chat_id)
        for member in members:
            if member.user_id == user_id:
                member.kicked = datetime.now()
                return self.chat_member_repo.delete(user_id)
        return None

    @staticmethod
    def is_owner(owner, chat):
        if owner.pk == chat.user:
            return True
        return False

    def is_member(self, user, chat):
        params = {
            'user': user,
            'chat': chat,
        }
        chat_member = self.chat_member_repo.filer_by(params)
        if chat_member.kicked:
            return False
        return True

    def add_member_to_chat(self, member: ChatMember):
        return self.create_members(member)


if __name__ == '__main__':
   c = ChatsChange(id=1, title='sss')
   print(c.dict())
   from application.dataclases import Chat
   cl = c.dict()
   ch = Chat(**cl)
   print(ch)
