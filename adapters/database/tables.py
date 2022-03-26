from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Float, ForeignKey
)
from sqlalchemy.orm import registry, relationship


mapper_registry = registry()
metadata = MetaData()
