from datetime import datetime

from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime
)

metadata = MetaData()

books = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(30), nullable=False),
    Column('author', String(30), nullable=False),
    Column('user', Integer, nullable=False, default=None),
    Column('created', DateTime, nullable=False, default=datetime.now),
)