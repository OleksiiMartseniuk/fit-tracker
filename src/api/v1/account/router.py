from fastapi import APIRouter, Depends, status

from src.account.controllers import UserController
from src.account.dependencies import get_user_controller
from src.account.dto import UserAddDTO, UserDTO
from src.api.v1.account.schemas import CreateUserSchema, UpdateUserSchema, UserSchema
from src.auth.dependencies import get_active_user

router = APIRouter(
    prefix="/account",
    tags=["Account"],
)


@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema,
)
async def create_user(
    data: CreateUserSchema,
    user_controller: UserController = Depends(get_user_controller),
):
    user = await user_controller.create_user(data=UserAddDTO(**data.model_dump()))
    return user.model_dump(exclude={"hashed_password"})


@router.get(
    "/user",
    response_model=UserSchema,
)
async def get_user(
    current_user: UserDTO = Depends(get_active_user),
    user_controller: UserController = Depends(get_user_controller),
):
    user = await user_controller.get_user(user_id=current_user.id)
    return user.model_dump(exclude={"hashed_password"})


@router.patch(
    "/user",
    response_model=UserSchema,
)
async def update_user(
    user_data: UpdateUserSchema,
    current_user: UserDTO = Depends(get_active_user),
    user_controller: UserController = Depends(get_user_controller),
):
    user = await user_controller.update_user(
        user_id=current_user.id,
        user_data=user_data,
    )
    return user.model_dump(exclude={"hashed_password"})


@router.delete(
    "/user",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    current_user: UserDTO = Depends(get_active_user),
    user_controller: UserController = Depends(get_user_controller),
):
    await user_controller.delete_user(user_id=current_user.id)
