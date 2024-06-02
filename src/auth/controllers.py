from datetime import timedelta

from fastapi import HTTPException, status
from injector import inject

from src.account.dto import Token
from src.auth.services.authentication import BaseAuthenticationService
from src.auth.services.jwt import BaseJWTService
from src.config import settings


class LoginController:
    @inject
    def __init__(
        self,
        authentication_service: BaseAuthenticationService,
        jwt_service: BaseJWTService,
    ):
        self.authentication_service = authentication_service
        self.jwt_service = jwt_service

    async def login_for_access_token(
        self,
        username: str,
        password: str,
    ) -> Token:
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

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.jwt_service.create_access_token(
            data={"user_id": user.id},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="Bearer")
