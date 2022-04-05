from classic.app.dto import DTO
from classic.components.component import component
from classic.messaging import Publisher, Message
from sqlalchemy.exc import InvalidRequestError

from adapters.message_bus.settings import RabbitConfigKombu
from application.book_aplication.dataclases import Book
from application.book_aplication.errors import BadRequest
from application.book_aplication.interfaces import BookRepositoryInterface


class BookDTO(DTO):
    title: str
    author: str
    user: int = None


class ChangeBook(DTO):
    id: int
    title: str = None
    author: str =None
    user: int = None


class SearchBook(DTO):
    id: int = None
    title: str = None
    author: str = None
    user: int = None


@component
class BookService:
    _repository: BookRepositoryInterface
    publisher: Publisher

    def _send_message(self, body: dict):
        message = {'message': body}
        self.publisher.plan(
            Message(RabbitConfigKombu.exchange.value, message)
        )

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

    def register(self, book: Book):
        book = self._repository.add(book)
        return book

    def create_book(self, data):
        book_dto = BookDTO(**data)
        cleaned_data = book_dto.dict()
        book = Book(**cleaned_data)
        new_book = self.register(book)
        id = new_book.id
        cleaned_data['id'] = id
        body = self.get_body(event='created', id=id, payload=cleaned_data)
        self._send_message(body=body)
        return new_book

    def get_book(self, pk):
        book = self._repository.get(pk)
        return book

    def get_books(self, limit=None, offset=None, **params):
        books = self._repository.get_list(limit=limit, offset=offset, **params)
        return books

    def filer_by(self, params):
        try:
            entity_model = self._repository.filer_by(params)
        except (InvalidRequestError, ):
            raise BadRequest()
        return entity_model

    @staticmethod
    def cleaned_data(data, model):
        validate_data = model(**data)
        cleaned_data = validate_data.dict()
        return cleaned_data

    def delete_book(self, data):
        cleaned_data = self.cleaned_data(data=data, model=ChangeBook)
        id = cleaned_data['id']
        deleted = self._repository.delete(id)
        if deleted:
            payload = {"deleted": f"book - {id} - success"}
            body = self.get_body(event='deleted', id=id, payload=payload)
            self._send_message(body=body)
        return deleted

    def update_book(self, data):
        cleaned_data = self.cleaned_data(data=data, model=ChangeBook)
        id = cleaned_data['id']
        prepare_data = {
            key: value for key, value in cleaned_data.items() if value is not None and key != 'id'
        }
        return self._repository.update(reference=id, params=prepare_data)

    def get_free_book(self, data):
        user = data.get('user')
        if not user:
            raise BadRequest()
        cleaned_data = self.cleaned_data(data=data, model=SearchBook)
        cleaned_data = {
            key: value for key, value in cleaned_data.items() if value is not None
        }
        cleaned_data['user'] = None
        book = self._repository.filer_by(cleaned_data)
        if not book:
            raise BadRequest()
        reference = book.id
        params = {"user": user}
        updated = self._repository.update(reference=reference, params=params)
        if not updated:
            raise BadRequest()
        payload = {"result": f"book - {reference} - take user {user}"}
        body = self.get_body(event='created', id=reference, payload=payload)
        self._send_message(body)
        return book

    def give_away_book(self, data):
        user = data.get('user')
        if not user:
            raise BadRequest()
        cleaned_data = self.cleaned_data(data=data, model=SearchBook)
        cleaned_data = {
            key: value for key, value in cleaned_data.items() if value is not None
        }
        cleaned_data['user'] = user
        book = self._repository.filer_by(cleaned_data)
        if not book:
            raise BadRequest()
        reference = book.id

        payload = {"result": f"book - {reference} - give away user {user}"}
        body = self.get_body(event='created', id=reference, payload=payload)

        params = {"user": None}
        updated = self._repository.update(reference=reference, params=params)
        if not updated:
            raise BadRequest()
        self._send_message(body)
        return book
