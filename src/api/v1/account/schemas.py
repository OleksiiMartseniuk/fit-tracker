from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]


class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
