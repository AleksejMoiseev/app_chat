from datetime import datetime

from sqlalchemy import (
    MetaData, Table, Column, Integer, VARCHAR, ForeignKey, Text, DateTime
)

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', VARCHAR(250)),
    Column('email', VARCHAR(250), nullable=False),
    Column('password', VARCHAR(250), nullable=False),
    Column('access_token', VARCHAR(250)),
    Column('refresh_token', VARCHAR(250)),
)

chats = Table(
    'chats', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('owner',  ForeignKey('users.id'), nullable=False),
    Column('descriptions', Text),
    Column('created', DateTime, nullable=False, default=datetime.now),
)

messages = Table(
    'messages', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id',  ForeignKey('users.id'), nullable=False),
    Column('chat_id', ForeignKey('chats.id'), nullable=False),
    Column('body', Text),
    Column('created', DateTime, nullable=False, default=datetime.now),
)

chatmembers = Table(
    'chatmembers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id',  ForeignKey('users.id'), nullable=False),
    Column('chat_id', ForeignKey('chats.id'), nullable=False),
    Column('checked_in', DateTime, nullable=False, default=datetime.now),
    Column('checked_out', DateTime),
    Column('kicked', DateTime),
)
