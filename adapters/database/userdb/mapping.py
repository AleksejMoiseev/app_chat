from sqlalchemy.orm import registry

from application.user_application import dataclases
from . import tables

mapper = registry()

mapper.map_imperatively(dataclases.User, tables.users)
