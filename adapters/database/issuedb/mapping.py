from sqlalchemy.orm import registry

from application.issue_aplication import dataclases
from . import tables

mapper = registry()

mapper.map_imperatively(dataclases.IssueUser, tables.issue_users)
mapper.map_imperatively(dataclases.IssueBook, tables.issue_books)
