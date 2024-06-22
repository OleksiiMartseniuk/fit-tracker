from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]


class CreateUserSchema(BaseModel):
    username: str = Field(min_length=4, max_length=30)
    password: str = Field(min_length=8, max_length=30)
    email: Optional[EmailStr] = None


class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(default=None, min_length=4, max_length=30)
    email: Optional[EmailStr] = None
