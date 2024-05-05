from datetime import datetime

from pydantic import BaseModel


class UserAddDto(BaseModel):
    username: str
    password: str


class UserDto(BaseModel):
    id: int
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None
