from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from injector import inject

from src.account.dto import UserDTO
from src.account.repository import UserRepository
from src.auth.services.jwt import BaseJWTService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


class AuthorizationJWTService:
    @inject
    def __init__(
        self,
        jwt_service: BaseJWTService,
        user_repository: UserRepository,
    ):
        self.jwt_service = jwt_service
        self.user_repository = user_repository

    async def authorize(self, token: str) -> UserDTO:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = self.jwt_service.decode_access_token(token=token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        user = await self.user_repository.get_or_none(id=user_id)
        if user is None:
            raise credentials_exception
        return user


class GetActiveUser(AuthorizationJWTService):
    async def get_active_user(self, token: str) -> UserDTO:
        user = await self.authorize(token=token)
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user

    async def __call__(self, token: Annotated[str, Depends(oauth2_scheme)]) -> UserDTO:
        return await self.get_active_user(token=token)
