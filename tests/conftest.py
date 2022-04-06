from unittest.mock import Mock

import pytest

from application.user_application import interfaces
from application.user_application.dataclases import User
from application.user_application.services import UserService


@pytest.fixture
def username_password():
    return "Alex", "password"


@pytest.fixture
def email():
    return "alex@mail.ru"


@pytest.fixture
def params(email, username_password):
    username, password = username_password
    return {
        'username': username,
        'email': email,
        'password': password,
        'access_token': None
    }


@pytest.fixture
def user(params):
    return User(**params)


@pytest.fixture
def user1(user):
    user.id = 0
    return user


@pytest.fixture
def users(params):
    actors = []
    for i in range(10):
        user = User(**params)
        user.id = i
        actors.append(user)
    return actors


@pytest.fixture(scope='function')
def user_repo(user, user1, users):
    user_repo = Mock(interfaces.UserRepositoryInterface)
    user_repo.add = Mock(return_value=user1)
    user_repo.get = Mock(return_value=user)
    user_repo.get_list = Mock(return_value=users)
    return user_repo


@pytest.fixture(scope='function')
def publisher():
    return "message"


@pytest.fixture
def user_service(user_repo):
    return UserService(repository=user_repo, publisher=publisher)


