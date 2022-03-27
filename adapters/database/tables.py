from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Float, ForeignKey, Date, Text
)
from sqlalchemy.orm import registry, relationship


mapper_registry = registry()
metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(30)),
    Column('email', String(30)),
    Column('password', String(30)),
    Column('access_token', String(128)),
    Column('refresh_token', String(128)),
)

chats = Table(
    'chats', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('owner',  ForeignKey('users.id')),
    Column('descriptions', Text),
    Column('created', Integer, Date),
)

messages = Table(
    'messages', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id',  ForeignKey('users.id')),
    Column('chat_id', ForeignKey('users.id')),
    Column('created', Integer, Date),
)
