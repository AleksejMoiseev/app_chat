from datetime import datetime

from classic.components.component import component
from sqlalchemy.exc import InvalidRequestError
from classic.messaging import Publisher, Message

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


class ChangeUser(DTO):
    id: int
    email: str = None
    password: str =None
    access_token: str = None
    refresh_token: str = None
    username: str = None


@component
class UserService:
    _repository: UserRepositoryInterface

    def register(self, user: User):
        user = self._repository.add(user)
        return user

    def create_user(self, data):
        user_dto = UserDTO(**data)
        cleaned_data = user_dto.dict()
        user = User(**cleaned_data)
        return self.user_service.register(user)

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

    @staticmethod
    def cleaned_data(data, model=ChangeUser):
        validate_data = model(**data)
        cleaned_data = validate_data.dict()
        return cleaned_data

    def delete_user(self, data):
        cleaned_data = self.cleaned_data(data=data)
        id = cleaned_data['id']
        return self._repository.delete(id)

    def update_user(self, data):
        cleaned_data = self.cleaned_data(data=data)
        id = cleaned_data['id']
        prepare_data = {
            key: value for key, value in cleaned_data.items() if value is not None and key != 'id'
        }
        return self._repository.update(reference=id, params=prepare_data)
