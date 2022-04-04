from datetime import datetime

from classic.components.component import component
from sqlalchemy.exc import InvalidRequestError
from classic.messaging import Publisher, Message

from application.book_aplication.dataclases import Book
from application.book_aplication.errors import BadRequest
from application.book_aplication.interfaces import BookRepositoryInterface
from classic.app.dto import DTO


class BookDTO(DTO):
    title: str
    author: str
    status: dict


class ChangeBook(DTO):
    id: int
    title: str = None
    author: str =None
    status: dict = None


@component
class BookService:
    _repository: BookRepositoryInterface

    def register(self, book: Book):
        book = self._repository.add(book)
        return book

    def create_book(self, data):
        book_dto = BookDTO(**data)
        cleaned_data = book_dto.dict()
        book = Book(**cleaned_data)
        return self.user_service.register(book)

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
    def cleaned_data(data, model=ChangeBook):
        validate_data = model(**data)
        cleaned_data = validate_data.dict()
        return cleaned_data

    def delete_book(self, data):
        cleaned_data = self.cleaned_data(data=data)
        id = cleaned_data['id']
        return self._repository.delete(id)

    def update_book(self, data):
        cleaned_data = self.cleaned_data(data=data)
        id = cleaned_data['id']
        prepare_data = {
            key: value for key, value in cleaned_data.items() if value is not None and key != 'id'
        }
        return self._repository.update(reference=id, params=prepare_data)
