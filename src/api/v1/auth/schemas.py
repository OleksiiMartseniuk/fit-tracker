from pydantic import BaseModel


class DataRefreshToken(BaseModel):
    refresh_token: str
