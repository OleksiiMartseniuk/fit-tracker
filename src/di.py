from functools import lru_cache

from injector import Binder, Injector, Module, singleton
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.controllers import UserController
from src.account.repository import UserRepository
from src.auth.controllers import LoginController
from src.auth.repository import TokenRepository
from src.auth.services.authentication import (
    AuthenticationService,
    BaseAuthenticationService,
)
from src.auth.services.authorization import AuthorizationJWTService
from src.auth.services.hash_password import BaseHashPasswordService, HashPasswordService
from src.auth.services.jwt import BaseJWTService, JWTService
from src.auth.services.token import BaseTokenService, TokenService
from src.database.base import async_session


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # DB
        binder.bind(AsyncSession, to=async_session, scope=singleton)
        # Repositories
        binder.bind(UserRepository, to=UserRepository, scope=singleton)
        binder.bind(TokenRepository, to=TokenRepository, scope=singleton)
        # Services
        binder.bind(BaseJWTService, to=JWTService, scope=singleton)
        binder.bind(BaseHashPasswordService, to=HashPasswordService, scope=singleton)
        binder.bind(
            BaseAuthenticationService,
            to=AuthenticationService,
            scope=singleton,
        )
        binder.bind(
            AuthorizationJWTService,
            to=AuthorizationJWTService,
            scope=singleton,
        )
        binder.bind(BaseTokenService, to=TokenService, scope=singleton)
        # Controllers
        binder.bind(LoginController, to=LoginController, scope=singleton)
        binder.bind(UserController, to=UserController, scope=singleton)


@lru_cache(maxsize=None)
def get_injector() -> Injector:
    return Injector([AppModule()])


injector = get_injector()
