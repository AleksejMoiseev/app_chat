from datetime import datetime

from sqlalchemy import (
    MetaData, Table, Column, Integer, DateTime, BOOLEAN
)

metadata = MetaData()

issue_users = Table(
    'issue_users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', Integer, nullable=False),
    Column('status', BOOLEAN, nullable=False, default=False),
    Column('created', DateTime, nullable=False, default=datetime.now),
)

issue_books = Table(
    'issue_books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book', Integer, nullable=False),
    Column('user', Integer, nullable=False, default=None),
    Column('status', BOOLEAN, nullable=False, default=True),
    Column('created', DateTime, nullable=False, default=datetime.now),
)