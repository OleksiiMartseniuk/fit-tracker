from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.controllers import LoginController
from src.auth.dependencies import get_login_controller
from src.auth.dto import Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    logen_controller: LoginController = Depends(get_login_controller),
):
    token = await logen_controller.login_for_access_token(
        username=form_data.username,
        password=form_data.password,
    )
    return token
