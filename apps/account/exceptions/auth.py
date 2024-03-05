from dataclasses import dataclass


@dataclass(eq=False)
class AuthorizationTokenServiceException(Exception):
    message: str


class UserDoesNotExistException(AuthorizationTokenServiceException):
    pass


class PasswordIncorrectException(AuthorizationTokenServiceException):
    pass


class TokenDontExistsException(AuthorizationTokenServiceException):
    pass
