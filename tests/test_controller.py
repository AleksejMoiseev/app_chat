import pytest

from composites.chat_api import user_service

Base_URL = 'http://127.0.0.1:8080/'


"""testing user service"""


def test_register_user(user):
    actor = user_service.register(user)
    assert actor.pk == 0


def test_get_user(user):
    actor = user_service.get_user(pk=0)
    assert actor.username == user.username
    assert actor.email == user.email
    assert actor.password == user.password
    assert actor.access_token == user.access_token


def test_get_users(users):
    users, size = users
    actors = []
    for actor in users:
        user_service.register(actor)
        actors.append(user_service.register(actor))
    assert len(actors) == size


@pytest.mark.parametrize('limit', [1, 2, 3])
def test_get_users_by_limit(limit):
    size = user_service.get_users(limit=limit)
    assert len(size) == limit


"""Testing MessageService"""