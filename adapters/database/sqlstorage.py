from classic.components.component import component
from classic.sql_storage.repository import BaseRepository
from sqlalchemy import select, desc, text, func

from application.interfaces import UserRepositoryInterface


@component
class UserPythonStructRepository(UserRepositoryInterface, BaseRepository):
    pass