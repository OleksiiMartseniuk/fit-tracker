from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from jwt.exceptions import InvalidTokenError

from src.config import settings


class BaseJWTService(ABC):
    @abstractmethod
    def create_access_token(
        self,
        data: dict,
        expires_delta: Union[timedelta, None] = None,
    ) -> str: ...

    @abstractmethod
    def decode_access_token(self, token: str) -> dict: ...


class JWTService(BaseJWTService):
    DEFAULT_EXPIRE_MINUTES = 15

    def create_access_token(
        self,
        data: dict,
        expires_delta: Union[timedelta, None] = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.DEFAULT_EXPIRE_MINUTES,
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
        except InvalidTokenError:
            return {}
