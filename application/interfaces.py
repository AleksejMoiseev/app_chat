import abc


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


class UserRepositoryInterface(abc.ABC, RepositoryInterface):
    pass


class ChatRepositoryInterface(abc.ABC, RepositoryInterface):
    pass


class ChatMembersRepositoryInterface(abc.ABC, RepositoryInterface):

    @abc.abstractmethod
    def get_members_by_chat(self, chat):
        pass


class MessageRepositoryInterface(abc.ABC, RepositoryInterface):
    pass


class ServiceInterface(abc.ABC):
    def __init__(self, repository: RepositoryInterface):
        self._repository = repository
