import abc


class UserRepositoryInterface(metaclass=abc.ABCMeta):

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

    @abc.abstractmethod
    def filer_by(self, params):
        pass

    @abc.abstractmethod
    def update(self, reference, params: dict):
        pass


class ServiceInterface(abc.ABC):
    def __init__(self, repository: UserRepositoryInterface):
        self._repository = repository
