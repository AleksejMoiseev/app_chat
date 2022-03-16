from adapters.storage import user_storage, message_storage
from application.dto import User, Message
from application.interfaces import ServiceInterface


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
    def register(self, message: Message):
        message = self._repository.add(message)
        return message

    def get_message(self, pk):
        user = self._repository.get(pk)
        return user

    def get_users(self, limit=None, offset=None, **params):
        users = self._repository.get_list(limit=limit, offset=offset, **params)
        return users


user_service = UserService(repository=user_storage)
message_service = MessageService(repository=message_storage)
