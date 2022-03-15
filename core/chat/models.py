from typing import Text

from core.models import BaseModel
from datetime import datetime


class Chat(BaseModel):

    def __init__(self, title: str, owner_id: int, descriptions: Text):
        super().__init__()
        self.title = title
        self.owner_id = owner_id
        self.descriptions = descriptions
        self.created = datetime.now()


class Message(BaseModel):

    def __init__(self, user_id, chat_id, body):
        super().__init__()
        self.user_id = user_id
        self.chat_id = chat_id
        self.body = body
        self.created = datetime.now()

