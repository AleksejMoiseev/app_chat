from core.storage import PythonStructRepository


class UserStorage(PythonStructRepository):
    def add(self, user):
        pk = getattr(user, 'pk', None)
        if pk is None:
            user.pk = max(self.db) + 1 if self.db else 0
        self.db[user.pk] = user
        return user

    def get(self, pk):
        pk = self.db.get(pk)
        return pk

    def get_list(self, limit: int = None, offset: int = None, **params):
        limit = limit or self.default_limit
        offset = offset or 0
        users = list(self.db.values())[offset: offset + limit]
        return users

    def delete(self, pk):
        user = self.db.pop(pk, None)
        return user

