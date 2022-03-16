from datetime import datetime
from typing import Text, Any

from pydantic import BaseModel


class Model(BaseModel):
    pk: int = None


class User(Model):
    username: str
    email: str
    password: str
    access_token: str = None
    refresh_token: str = None


class Chat(BaseModel):
    title: str
    owner_id: str
    descriptions: Text
    created = datetime.now()


class Message(BaseModel):
    user_id: int
    chat_id: int
    body: Text
    created = datetime.now()


if __name__ == '__main__':
    User(username='aaa', email='ssss', password='ssss')
    print(User)
