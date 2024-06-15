from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.account.dto import UserDTO
from src.auth.services.authentication import AuthenticationService
from src.auth.services.authorization import AuthorizationTokenService
from src.auth.services.token import BaseTokenService
from src.config import settings
from src.di import injector


class AdminAuth(AuthenticationBackend):
    def __init__(
        self,
        secret_key: str,
        authorization_token_service: AuthorizationTokenService,
        authentication_service: AuthenticationService,
        token_service: BaseTokenService,
    ):
        super().__init__(secret_key=secret_key)
        self.authorization_token_service = authorization_token_service
        self.authentication_service = authentication_service
        self.token_service = token_service

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        user = await self.authentication_service.authenticate_user(
            username=username,
            password=password,
        )
        if not user:
            return False

        if not self._check_user_permission(user=user):
            return False

        token = await self.token_service.get_or_create(user_id=user.id)
        request.session.update({"token": token.token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        user = await self.authorization_token_service.authorize(token=token)
        if not user:
            return False

        if not self._check_user_permission(user=user):
            return False

        return True

    @staticmethod
    def _check_user_permission(user: UserDTO) -> bool:
        if not user.is_superuser:
            return False
        return True


authentication_backend = AdminAuth(
    secret_key=settings.ADMIN_SECRET_KEY,
    authorization_token_service=injector.get(AuthorizationTokenService),
    authentication_service=injector.get(AuthenticationService),
    token_service=injector.get(BaseTokenService),
)
