import abc
from collections import defaultdict


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


_registry = defaultdict(dict)


class PythonStructRepository(RepositoryInterface):
    def __init__(self, namespace, default_limit=20):
        self.db = _registry[namespace]
        self.default_limit = default_limit

    def add(self, entity):
        pk = getattr(entity, 'pk', None)
        if pk is None:
            entity.pk = max(self.db) + 1 if self.db else 0
        self.db[entity.pk] = entity
        return entity

    def get(self, pk):
        entity = self.db.get(pk)
        return entity

    def get_list(self, limit: int = None, offset: int = None, **params):
        limit = limit or self.default_limit
        offset = offset or 0
        entities = list(self.db.values())[offset: offset + limit]
        return entities

    def delete(self, pk):
        entity = self.db.pop(pk, None)
        return entity


user_storage = PythonStructRepository('users')
message_storage = PythonStructRepository('message')
chat_storage = PythonStructRepository('chat')
chat_member_storage = PythonStructRepository("chat_member")
