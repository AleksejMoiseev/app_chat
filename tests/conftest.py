from unittest.mock import Mock

import pytest

from application.user_application import interfaces
from application.user_application.dataclases import User
from application.user_application.services import UserService

ACCESS_TOKEN = " Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwayI6MH0.99Q7zHnAZVqblwg93gjXYRCB-LmOuhfWjWWqx0ei5fg"
REFRESH_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" \
                ".eyJleHAiOjE2NDc1ODcxNzJ9.H2gTn-_QYxegb8lO7yHFpk-ntZN7hp0X5jDt6fU0izk"


@pytest.fixture
def username_password():
    return "Alex", "password"


@pytest.fixture
def email():
    return "alex@mail.ru"


@pytest.fixture
def headers_auth():
    headers = {'Authorization': ACCESS_TOKEN}
    return headers


@pytest.fixture
def params(email, username_password):
    username, password = username_password
    return {
        'username': username,
        'email': email,
        'password': password,
        'access_token': ACCESS_TOKEN
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


