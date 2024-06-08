from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from jwt.exceptions import InvalidTokenError

from src.config import settings


class BaseJWTService(ABC):
    @abstractmethod
    def _create_token(
        self,
        data: dict,
        expires_delta: timedelta,
    ) -> str: ...

    @abstractmethod
    def create_access_token(
        self,
        data: dict,
        expires_delta: Union[timedelta, None] = None,
    ) -> str: ...

    @abstractmethod
    def create_refresh_token(
        self,
        data: dict,
        expires_delta: Union[timedelta, None] = None,
    ) -> str: ...

    @abstractmethod
    def decode_access_token(self, token: str) -> dict: ...


class JWTService(BaseJWTService):
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    def _create_token(
        self,
        data: dict,
        expire: datetime,
    ) -> str:
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return encoded_jwt

    def create_access_token(
        self,
        data: dict,
        expires_delta: Union[timedelta, None] = None,
    ) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES,
            )
        return self._create_token(data=data, expire=expire)

    def create_refresh_token(
        self,
        data: dict,
        expires_delta: Union[timedelta, None] = None,
    ) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                days=self.REFRESH_TOKEN_EXPIRE_DAYS,
            )
        return self._create_token(data=data, expire=expire)

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
        except InvalidTokenError:
            return {}
