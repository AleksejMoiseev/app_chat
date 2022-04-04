from datetime import datetime

from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime
)

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(30)),
    Column('email', String(30), nullable=False),
    Column('password', String(30), nullable=False),
    Column('access_token', String(128)),
    Column('refresh_token', String(128)),
    Column('created', DateTime, nullable=False, default=datetime.now),
)