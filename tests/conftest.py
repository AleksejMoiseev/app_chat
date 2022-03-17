import pytest

ACCESS_TOKEN = " Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwayI6MH0.99Q7zHnAZVqblwg93gjXYRCB-LmOuhfWjWWqx0ei5fg"
REFRESH_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" \
                ".eyJleHAiOjE2NDc1ODcxNzJ9.H2gTn-_QYxegb8lO7yHFpk-ntZN7hp0X5jDt6fU0izk"


@pytest.fixture
def login_password():
    return "login", "password"


@pytest.fixture
def email():
    return "alex@mail.ru"


@pytest.fixture
def headers_auth():
    headers = {'Authorization': ACCESS_TOKEN}
    return headers



