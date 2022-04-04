from dataclasses import field, dataclass
from datetime import datetime


@dataclass
class BaseModel:
    id: int = field(init=False)


@dataclass
class IssueUser(BaseModel):
    user: int
    status: bool = field(default=False)
    created: datetime = field(default_factory=datetime.now)


@dataclass
class IssueBook(BaseModel):
    book: int
    user: int = field(default=None)
    status: bool = field(default=True)
    created: datetime = field(default_factory=datetime.now)
