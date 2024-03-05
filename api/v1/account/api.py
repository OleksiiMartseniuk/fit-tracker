from ninja import Router

from api.v1.account.schemas import LoginSchema, TokenSchema, UserSchema
from apps.account.exceptions.auth import AuthorizationTokenServiceException
from apps.account.services.auth import AuthorizationTokenService
from apps.account.services.security import AuthBearer
from apps.utils.schemas import MassageError

router = Router(tags=["account"])


@router.post("login", response={200: TokenSchema, 401: MassageError})
def login(request, login_data: LoginSchema):
    try:
        token = AuthorizationTokenService().authorization(**login_data.model_dump())
        return 200, TokenSchema(access_token=token)
    except AuthorizationTokenServiceException as e:
        return 401, MassageError(detail=e.message, status_code=401)


@router.get("logout", auth=AuthBearer(), response={200: None, 401: MassageError})
def logout(request):
    try:
        AuthorizationTokenService().logout(request.auth)
    except AuthorizationTokenServiceException as e:
        return 401, MassageError(detail=e.message, status_code=401)


@router.get("user", auth=AuthBearer(), response={200: UserSchema})
def get_user(request):
    return 200, request.auth
