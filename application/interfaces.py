import abc
from datetime import datetime


class RepositoryInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError

    @abc.abstractmethod
    def get_list(self, limit: int = None, offset: int = None, **params):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, reference):
        raise NotImplementedError


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
