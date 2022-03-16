import abc
from datetime import datetime

from adapters.storage import RepositoryInterface
from application.dto import User, Message
#from application.services import ChatMemberService, ChatService, MessageService


class ServiceInterface(abc.ABC):
    def __init__(self, repository: RepositoryInterface):
        self._repository = repository


# class ChatInteractor:
#     def __init__(self, chat_member: ChatMemberService, chat: ChatService, message: MessageService,):
#         self.chat_member = chat_member
#         self.chat = chat
#         self.message = message
#
#     def create_chat(self, user: User):
#         pass
#
#     def past_message(self, interval: datetime, chat_id: int):
#         pass
#
#     def send_message(self, message: Message):
#         pass
#
#     def get_members_by_chat(self, chat_id):
#         pass
