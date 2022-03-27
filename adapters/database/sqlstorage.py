from classic.components.component import component
from classic.sql_storage.repository import BaseRepository
from sqlalchemy import select, desc, text, func

from application.interfaces import RepositoryInterface
from application.dataclases import BaseModel, User, Message, Chat, ChatMember


@component
class SQLBaseRepository(RepositoryInterface, BaseRepository):
    model: BaseModel
    default_limit: int

    def add(self, entity):
        entity_model = self.session.query(self.model).filter_by(id=entity.id).one_or_none()
        if entity_model:
            return entity_model
        self.session.add(entity)
        self.session.flush()
        return entity

    def get(self, reference):
        return self.session.query(self.model).filter_by(id=reference).one_or_none()

    def get_list(self, limit: int = None, offset: int = None, **params):
        limit = limit or self.default_limit
        offset = offset or 0
        query = select(self.model)
        return self.session.execute(query).scalars().all()[offset: offset + limit]

    def delete(self, reference):
        result = self.session.query(self.model).filter(self.model.id == reference).delete()
        self.session.flush()
        return result


@component
class UserRepository(SQLBaseRepository):
    model: User
    default_limit: int


@component
class ChatRepository(SQLBaseRepository):
    model: Chat
    default_limit: int


@component
class ChatMemberRepository(SQLBaseRepository):
    model: ChatMember
    default_limit: int


@component
class MessageRepository(SQLBaseRepository):
    model: Message
    default_limit: int
