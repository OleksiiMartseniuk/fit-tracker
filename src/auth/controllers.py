from datetime import timedelta

from fastapi import HTTPException, status
from injector import inject

from src.account.repository import UserRepository
from src.auth.dto import JWTTokenDTO
from src.auth.services.authentication import BaseAuthenticationService
from src.auth.services.jwt import BaseJWTService
from src.config import settings


class LoginController:
    @inject
    def __init__(
        self,
        authentication_service: BaseAuthenticationService,
        jwt_service: BaseJWTService,
        user_repository: UserRepository,
    ):
        self.authentication_service = authentication_service
        self.jwt_service = jwt_service
        self.user_repository = user_repository

    async def create_token(self, user_id: int) -> JWTTokenDTO:
        access_token = self.jwt_service.create_access_token(
            data={"user_id": user_id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = self.jwt_service.create_refresh_token(
            data={"_user_id": user_id},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return JWTTokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )

    async def login_for_access_token(
        self,
        username: str,
        password: str,
    ) -> JWTTokenDTO:
        user = await self.authentication_service.authenticate_user(
            username=username,
            password=password,
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await self.create_token(user_id=user.id)

    async def refresh_access_token(self, refresh_token: str) -> JWTTokenDTO:
        payload = self.jwt_service.decode_access_token(token=refresh_token)
        user_id = payload.get("_user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await self.user_repository.get_or_none(id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await self.create_token(user_id=user.id)
