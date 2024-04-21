from injector import Binder, Module, singleton

from domain.account.repository import TokeDjangoRepository, UserDjangoRepository
from domain.account.services.auth import (
    AuthorizationTokenService,
    BaseAuthorizationService,
)
from domain.account.services.token import BaseTokeService, TokenService


class AuthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(TokeDjangoRepository, scope=singleton)
        binder.bind(UserDjangoRepository, scope=singleton)
        binder.bind(BaseTokeService, to=TokenService, scope=singleton)
        binder.bind(
            BaseAuthorizationService, to=AuthorizationTokenService, scope=singleton
        )
