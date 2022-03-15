from core.service_interfaces import ServiceInterface
from users.models import User
from users.storage import UserStorage


class UserService(ServiceInterface):
    def register(self, user: User):
        user = self._repository.add(user)
        return user

    def get_user(self, pk):
        user = self._repository.get(pk)
        return user

    def get_users(self, limit=None, offset=None, **params):
        users = self._repository.get_list(limit=limit, offset=offset, **params)
        return users


table_user = UserStorage('users')

USER_ORM = UserService(repository=table_user)


if __name__ == '__main__':
    pass
    # USER_STORAGE = UserStorage(namespace="users")
    # USER_ORM = UserService(repository=USER_STORAGE)
    # params = {'username': "Alex", 'email': 'alex@mail.ru', 'password': "qqqqq"}
    # user = User(**params)
    # USER_ORM.register(user)
    # user = USER_ORM.get_users()[0]
    # print(user.pk)
    # user1 = User(**params)
    # USER_ORM.register(user1)
    # user1 = USER_ORM.get_users()[1]
    # print(user1.pk, user.pk)