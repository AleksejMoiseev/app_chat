from dataclasses import dataclass
from dataclasses import field
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


@dataclass
class Chat(BaseModel):
    user: User
    descriptions: Text = None
    title: str = None
    created: datetime = field(default_factory=datetime.now)


@dataclass
class Message(BaseModel):
    user: User
    chat: Chat
    body: Text
    created: datetime = field(default_factory=datetime.now)


@dataclass
class ChatMember(BaseModel):
    user: User
    chat: Chat
    checked_in: datetime = field(default_factory=datetime.now)
    checked_out: datetime = None
    kicked: datetime = None


if __name__ == '__main__':
    d = {'email': 'Alex@bk.ru', 'password': 'password', 'access_token': None, 'refresh_token': None, 'username': 'Alex'}
    u = User(email=d['email'], password=d['password'])
    print(u)

