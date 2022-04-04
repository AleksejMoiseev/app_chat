from classic.components.component import component
from classic.sql_storage.repository import BaseRepository
from sqlalchemy import select

from application.user_application.dataclases import BaseModel, User
from application.interfaces import RepositoryInterface


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

    def filer_by(self, params: dict):
        entity_model = self.session.query(self.model).filter_by(**params).one_or_none()
        return entity_model

    def update(self, reference, params: dict):
        result = self.session.query(self.model).filter_by(id=reference).update(params, synchronize_session='fetch')
        self.session.flush()
        return result


@component
class UserRepository(SQLBaseRepository):
    model: User
    default_limit: int
