import requests
from http import HTTPStatus


Base_URL = 'http://127.0.0.1:8080/'


def test_positive_create_chat(expected_value_for_create):
    assert expected_value_for_create == {"id": 1, "name": 'issue_Alex'}


def test_create_chat(headers_auth):
    prefix = 'chats'
    path = Base_URL + prefix
    params = {
        'title': 'title',
        'descriptions': 'descriptions',
    }

    resp = requests.post(path, params, headers=headers_auth)
    assert resp.status_code == 201
