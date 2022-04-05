from classic.app.dto import DTO
from classic.components.component import component
from classic.messaging import Message
from classic.messaging import Publisher
from sqlalchemy.exc import InvalidRequestError

from adapters.message_bus.settings import ExchangeTopic
from application.errors import BadRequest
from application.user_application.dataclases import User
from application.user_application.interfaces import UserRepositoryInterface


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


"""
body = {
    'event': str,
    'service': str,
    'id': int,
    'payload':{}
}
"""


@component
class UserService:
    _repository: UserRepositoryInterface
    publisher: Publisher

    def _send_message(self, body: dict):
        message = {'message': body}
        self.publisher.plan(
            Message(ExchangeTopic.exchange.value, message)
        )

    def register(self, user: User):
        user = self._repository.add(user)
        return user

    @staticmethod
    def get_body(event, payload, id, service='user'):
        events = ['created', 'updated', 'deleted', 'gets']
        if event not in events:
            raise BadRequest()
        body = {
            "event": event,
            "service": service,
            "data": id,
            "payload": payload
        }
        return body

    def create_user(self, data):
        user_dto = UserDTO(**data)
        cleaned_data = user_dto.dict()
        user = User(**cleaned_data)
        new_user = self.register(user)
        id = new_user.id
        cleaned_data['id'] = id
        body = self.get_body(event='created', id=id, payload=cleaned_data)
        self._send_message(body=body)
        return self.register(user)

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
        deleted = self._repository.delete(id)
        if deleted:
            payload = {"deleted": f"user - {id} - success"}
            body = self.get_body(event='deleted', id=id, payload=payload)
            self._send_message(body=body)
        return deleted

    def update_user(self, data):
        cleaned_data = self.cleaned_data(data=data)
        id = cleaned_data['id']
        prepare_data = {
            key: value for key, value in cleaned_data.items() if value is not None and key != 'id'
        }
        return self._repository.update(reference=id, params=prepare_data)
