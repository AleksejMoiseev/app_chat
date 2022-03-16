import abc

from core.storage import RepositoryInterface


class ServiceInterface(abc.ABC):
    def __init__(self, repository: RepositoryInterface):
        self._repository = repository
