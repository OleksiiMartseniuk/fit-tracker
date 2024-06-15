from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class JWTTokenDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenDTO(BaseModel):
    id: int
    token: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
