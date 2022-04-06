from dataclasses import field, dataclass
from datetime import datetime


@dataclass
class BaseModel:
    id: int = field(init=False)


@dataclass
class User(BaseModel):
    email: str
    password: str
    access_token: str = None
    refresh_token: str = None
    username: str = None
    created: datetime = field(default_factory=datetime.now)
