from ninja_extra import NinjaExtraAPI, status

from api.v1.account.controller import AuthenticationController, UserController
from apps.account.security import InvalidToken

api = NinjaExtraAPI()


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return api.create_response(
        request=request,
        data={"detail": "Invalid token supplied"},
        status=status.HTTP_401_UNAUTHORIZED,
    )


api.register_controllers(
    AuthenticationController,
    UserController,
)
