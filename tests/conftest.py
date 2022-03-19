import datetime
from unittest.mock import Mock

import pytest

from application import interfaces
from application.dto import User, Chat, Message, ChatMember
from application.services import UserService, MessageService, ChatService, ChatMemberService

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
def user1():
    return User(
        pk=0,
        username='Alex',
        email='alex@mail.ru',
        password='password',
        access_token=ACCESS_TOKEN,
    )


@pytest.fixture
def users(params):
    actors = []
    for i in range(10):
        actors.append(User(pk=i, **params))
    return actors


@pytest.fixture
def owner(user):
    user.pk = 0
    return user


@pytest.fixture(scope='function')
def user_repo(user, user1, users):
    user_repo = Mock(interfaces.UserRepositoryInterface)
    user_repo.add = Mock(return_value=user1)
    user_repo.get = Mock(return_value=user)
    user_repo.get_list = Mock(return_value=users)
    return user_repo


@pytest.fixture
def user_service(user_repo):
    return UserService(repository=user_repo)


@pytest.fixture
def message():
    params = {
        'user_id': 0,
        'chat_id': 0,
        'body': "Hello"
    }
    return Message(**params)


@pytest.fixture
def message0():
    params = {
        'pk': 0,
        'user_id': 0,
        'chat_id': 0,
        'body': "Hello"
    }
    return Message(**params)


@pytest.fixture
def messages():
    params = {
        'user_id': 0,
        'chat_id': 0,
        'body': "Hello"
    }
    ms = []
    for i in range(10):
        ms.append(Message(pk=i, **params))
    return ms


@pytest.fixture(scope='function')
def message_repo(message0, messages):
    message_repo = Mock(interfaces.MessageRepositoryInterface)
    message_repo.add = Mock(return_value=message0)
    message_repo.get = Mock(return_value=message0)
    message_repo.get_list = Mock(return_value=messages)
    return message_repo


@pytest.fixture
def message_service(message_repo):
    return MessageService(messages_repo=message_repo)


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


@pytest.fixture
def chat0(params_chat):
    return Chat(pk=0, **params_chat)


@pytest.fixture
def chats(params_chat):
    chs = []
    for i in range(10):
        chs.append(Chat(pk=i, **params_chat))
    return chs


@pytest.fixture(scope='function')
def chat_repo(chat0, chats):
    chat_repo = Mock(interfaces.ChatRepositoryInterface)
    chat_repo.add = Mock(return_value=chat0)
    chat_repo.get = Mock(return_value=chat0)
    chat_repo.get_list = Mock(return_value=chats)
    chat_repo.delete = Mock(return_value=chat0)
    return chat_repo




@pytest.fixture
def chat_member_params():
    return {
        'user_id': 0,
        'chat_id': 0,
    }


@pytest.fixture
def chat_member(chat_member_params):
    return ChatMember(**chat_member_params)


@pytest.fixture
def chat_member0(chat_member_params):
    return ChatMember(pk=0, **chat_member_params)


@pytest.fixture
def chat_members(chat_member_params):
    cms = []
    for i in range(10):
        cms.append(ChatMember(pk=i, **chat_member_params))
    cms[0].kicked = datetime.datetime.now()
    cms[-1].kicked = datetime.datetime.now()
    return cms


@pytest.fixture(scope='function')
def chat_member_repo(chat_member0, chat_members):
    chat_member_repo = Mock(interfaces.ChatMembersRepositoryInterface)
    chat_member_repo.add = Mock(return_value=chat_member0)
    chat_member_repo.get = Mock(return_value=chat_member0)
    chat_member_repo.get_list = Mock(return_value=chat_members)
    chat_member_repo.delete = Mock(return_value=chat_member0)
    return chat_member_repo


@pytest.fixture(scope='function')
def chat_member_service(chat_member_repo):
    return ChatMemberService(chat_member_repo=chat_member_repo)


@pytest.fixture(scope='function')
def chat_service(chat_repo, chat_member_repo):
    return ChatService(chats_repo=chat_repo, members_repo=chat_member_repo)

