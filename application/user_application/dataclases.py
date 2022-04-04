from dataclasses import field, dataclass
from datetime import datetime
from typing import Text


@dataclass
class BaseModel:
    id: int = field(init=False)


@dataclass
class User(BaseModel):
    email: str
    password: str
    access_token: str = None
    refresh_token: str = None
    username: str = None
    created: datetime = field(default_factory=datetime.now)


if __name__ == '__main__':
    d = {'email': 'Alex@bk.ru', 'password': 'password', 'access_token': None, 'refresh_token': None, 'username': 'Alex'}
    user = User(email=d['email'], password=d['password'])
    print(user)
