import pytest
from application.dto import User, Chat

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
def users(params):
    actors = []
    for i in range(10):
        actors.append(User(**params))
    return actors, len(actors)


@pytest.fixture
def owner(user):
    user.pk = 0
    return user


@pytest.fixture
def params_chat(owner):
    return {
        'title': "title",
        'descriptions': 'descriptions',
        'owner': owner.pk
    }


@pytest.fixture
def chat(params_chat):
    return Chat(**params_chat)




def params_message(user, ):
    return {

    }



