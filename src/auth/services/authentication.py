from abc import ABC, abstractmethod
from typing import Union

from injector import inject

from src.account.dto import UserDTO
from src.account.repository import UserRepository
from src.auth.services.hash_password import BaseHashPasswordService


class BaseAuthenticationService(ABC):
    def __init__(
        self,
        hash_password_service: BaseHashPasswordService,
        user_repository: UserRepository,
    ):
        self.hash_password_service = hash_password_service
        self.user_repository = user_repository

    @abstractmethod
    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> Union[UserDTO, None]: ...


class AuthenticationService(BaseAuthenticationService):
    @inject
    def __init__(
        self,
        hash_password_service: BaseHashPasswordService,
        user_repository: UserRepository,
    ):
        super().__init__(
            hash_password_service=hash_password_service,
            user_repository=user_repository,
        )

    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> Union[UserDTO, None]:
        user = await self.user_repository.get_or_none(username=username)
        if not user:
            return None
        if not self.hash_password_service.verify_password(
            plain_password=password,
            hashed_password=user.hashed_password,
        ):
            return None
        return user
