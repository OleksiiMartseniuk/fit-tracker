from ninja_extra import ControllerBase, api_controller, http_get, route, status

from api.v1.account.schemas import LoginSchema, TokenSchema, UserSchema
from apps.account.security import AuthBearer
from apps.utils.schemas import MassageError
from domain.account.services.auth import AuthorizationTokenService
from domain.base.exception import BaseApplicationException


@api_controller("auth")
class AuthenticationController(ControllerBase):
    def __init__(self, authorization_token_service: AuthorizationTokenService):
        self.authorization_token_service = authorization_token_service

    @route.post(
        "login",
        response={
            status.HTTP_200_OK: TokenSchema,
            status.HTTP_401_UNAUTHORIZED: MassageError,
        },
    )
    def login(self, request, login_data: LoginSchema):
        try:
            token = self.authorization_token_service.authorization(
                **login_data.model_dump(),
            )
            return status.HTTP_200_OK, TokenSchema(access_token=token)
        except BaseApplicationException as e:
            return (
                status.HTTP_401_UNAUTHORIZED,
                MassageError(
                    detail=e.message,
                    status_code=status.HTTP_401_UNAUTHORIZED,
                ),
            )

    @route.get(
        "logout",
        auth=AuthBearer(),
        response={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED: MassageError,
        },
    )
    def logout(self, request):
        try:
            self.authorization_token_service.logout(request.user.id)
        except BaseApplicationException as e:
            return (
                status.HTTP_401_UNAUTHORIZED,
                MassageError(detail=e.message, status_code=401),
            )


@api_controller("user", auth=AuthBearer())
class UserController(ControllerBase):
    @http_get("", response=UserSchema)
    def get_user(self, request):
        return request.user.__dict__
