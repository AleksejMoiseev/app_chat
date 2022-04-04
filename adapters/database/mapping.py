from sqlalchemy.orm import registry, relationship
from application import dataclases

from . import tables

mapper = registry()


mapper.map_imperatively(dataclases.Chat, tables.chats, properties={
    'user': relationship(dataclases.User,
                         uselist=False),
})

mapper.map_imperatively(dataclases.Message, tables.messages, properties={
    'user': relationship(dataclases.User,
                         uselist=False, lazy='joined'),
    'chat': relationship(dataclases.Chat,
                         uselist=False, lazy='joined'),
})

mapper.map_imperatively(dataclases.ChatMember, tables.chatmembers, properties={
    'user': relationship(dataclases.User,
                         uselist=False, lazy='joined'),
    'chat': relationship(dataclases.Chat,
                         uselist=False, lazy='joined'),
})
