from injector import inject

from src.account.dto import UserAddDTO, UserDTO
from src.account.repository import UserRepository
from src.account.services.user import UserService
from src.api.v1.account.schemas import UpdateUserSchema


class UserController:
    @inject
    def __init__(self, user_service: UserService, user_repository: UserRepository):
        self.user_service = user_service
        self.user_repository = user_repository

    async def create_user(self, data: UserAddDTO) -> UserDTO:
        user = await self.user_service.create_user(data)
        return user

    async def get_user(self, user_id: int):
        user = await self.user_repository.get(id=user_id)
        return user

    async def update_user(self, user_id: int, user_data: UpdateUserSchema) -> UserDTO:
        user_dict = user_data.model_dump(exclude_none=True)
        if user_dict:
            await self.user_repository.update(data=user_dict, id=user_id)

        user = await self.user_repository.get(id=user_id)
        return user

    async def delete_user(self, user_id: int) -> None:
        await self.user_repository.delete(id=user_id)
