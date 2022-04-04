from sqlalchemy.orm import registry

from application.book_aplication import dataclases
from . import tables

mapper = registry()

mapper.map_imperatively(dataclases.Book, tables.books)
