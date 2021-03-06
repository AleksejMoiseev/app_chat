from datetime import datetime
from typing import Text

from pydantic import BaseModel, Field


class Model(BaseModel):
    pk: int = None

    def __str__(self):
        return f"{self.pk}"


class User(Model):
    username: str
    email: str
    password: str
    access_token: str = None
    refresh_token: str = None


class Chat(Model):
    title: str
    user: int
    descriptions: Text
    created: datetime = Field(default_factory=datetime.now)

    def __str__(self):
        return f"{self.pk}"


class Message(Model):
    user_id: int
    chat_id: int
    body: Text
    created: datetime = Field(default_factory=datetime.now)


class ChatMember(Model):
    user_id: int
    chat_id: int
    checked_in: datetime = Field(default_factory=datetime.now)
    checked_out: datetime = None
    kicked: datetime = None
