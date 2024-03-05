from ninja import NinjaAPI

from api.v1.account.api import router as account
from apps.account.services.security import InvalidToken

api = NinjaAPI()


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return api.create_response(
        request=request,
        # add message pydantic
        data={"detail": "Invalid token supplied"},
        status=401,
    )


api.add_router("/account/", account)
