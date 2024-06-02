from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserAddDTO(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


class UserDTO(BaseModel):
    id: int
    username: str
    hashed_password: str
    email: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
