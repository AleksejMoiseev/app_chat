from datetime import datetime

from classic.app.dto import DTO
from classic.components.component import component
from sqlalchemy.exc import InvalidRequestError
from classic.messaging import Publisher, Message
from adapters.message_bus.settings import ExchangeTopic

from application.user_application.dataclases import User
from application.errors import BadRequest
from application.user_application.interfaces import UserRepositoryInterface
from classic.app.dto import DTO


class UserDTO(DTO):
    email: str
    password: str
    access_token: str = None
    refresh_token: str = None
    username: str = None


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

    def delete_user(self, id):
        return self._repository.delete(id)
