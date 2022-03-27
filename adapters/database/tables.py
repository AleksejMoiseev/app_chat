from datetime import datetime

from sqlalchemy import (
    MetaData, Table, Column, Integer, String, ForeignKey, Text, DateTime
)

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
    Column('created', DateTime, nullable=False, default=datetime.now),
)

messages = Table(
    'messages', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id',  ForeignKey('users.id')),
    Column('chat_id', ForeignKey('chats.id')),
    Column('body', Text),
    Column('created', DateTime, nullable=False, default=datetime.now),
)

chatmembers = Table(
    'chatmembers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id',  ForeignKey('users.id')),
    Column('chat_id', ForeignKey('chats.id')),
    Column('checked_in', DateTime, nullable=False, default=datetime.now),
    Column('checked_out', DateTime),
    Column('kicked', DateTime),
)
