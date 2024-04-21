from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenDTO:
    user: int
    access_token: str


@dataclass
class UserDTO:
    id: int
    username: str
    password: str
    email: str | None
    first_name: str | None
    last_name: str | None
    is_superuser: bool
    is_active: bool
    is_staff: bool
    date_joined: datetime
