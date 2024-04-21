from abc import ABC, abstractmethod

from injector import inject

from domain.account.exceptions import PasswordIncorrectException
from domain.account.repository import UserDjangoRepository
from domain.account.services.token import TokenService


class BaseAuthorizationService(ABC):
    def __init__(
        self,
        user_repository: UserDjangoRepository,
        token_service: TokenService,
    ):
        self.user_repository = user_repository
        self.token_service = token_service

    @abstractmethod
    def authorization(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def logout(self, user_id: int) -> None:
        pass


class AuthorizationTokenService(BaseAuthorizationService):
    @inject
    def __init__(
        self,
        user_repository: UserDjangoRepository,
        token_service: TokenService,
    ):
        super().__init__(
            user_repository,
            token_service,
        )

    def authorization(self, username: str, password: str) -> str:
        user = self.user_repository.get(username=username)

        if not self.user_repository.check_password(password=password, id=user.id):
            raise PasswordIncorrectException(
                f"Password for user {username} is incorrect",
            )

        access_token = self.token_service.get_or_create_token(user_id=user.id)
        return access_token

    def logout(self, user_id: int) -> None:
        self.user_repository.delete_auth_token(user_id=user_id)
