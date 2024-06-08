from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.v1.auth.schemas import DataRefreshToken
from src.auth.controllers import LoginController
from src.auth.dependencies import get_login_controller
from src.auth.dto import Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/jwt/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    logen_controller: LoginController = Depends(get_login_controller),
):
    token = await logen_controller.login_for_access_token(
        username=form_data.username,
        password=form_data.password,
    )
    return token


@router.post("/jwt/refresh", response_model=Token)
async def refresh_access_token(
    data_refresh_token: DataRefreshToken,
    logen_controller: LoginController = Depends(get_login_controller),
):
    token = await logen_controller.refresh_access_token(
        refresh_token=data_refresh_token.refresh_token
    )
    return token
