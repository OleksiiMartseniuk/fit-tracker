from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    email: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
