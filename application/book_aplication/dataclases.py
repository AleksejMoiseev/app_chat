from dataclasses import field, dataclass
from datetime import datetime


@dataclass
class BaseModel:
    id: int = field(init=False)


@dataclass
class Book(BaseModel):
    title: str
    author: str
    status: dict
    created: datetime = field(default_factory=datetime.now)
