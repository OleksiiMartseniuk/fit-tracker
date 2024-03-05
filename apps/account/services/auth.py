from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from apps.account.exceptions.auth import (
    PasswordIncorrectException,
    TokenDontExistsException,
    UserDoesNotExistException,
)
from apps.account.models import Token

User = get_user_model()


class BaseAuthorizationService(ABC):
    @abstractmethod
    def authorization(self, *args, **kwargs) -> str:
        pass

    @abstractmethod
    def logout(self, *args, **kwargs) -> None:
        pass


class AuthorizationTokenService(BaseAuthorizationService):
    def authorization(self, username: str, password: str) -> str:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise UserDoesNotExistException(
                f"User with username {username} does not found",
            )

        if not user.check_password(password):
            raise PasswordIncorrectException(
                f"Password for user {username} is incorrect",
            )

        token, _ = Token.objects.get_or_create(
            user=user,
            defaults={"access_token": get_random_string(50)},
        )
        return token.access_token

    def logout(self, user: User) -> None:
        if not hasattr(user, "auth_token"):
            raise TokenDontExistsException(
                f"User {user.username} does not have token to logout",
            )
        user.auth_token.delete()
