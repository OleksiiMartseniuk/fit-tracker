from abc import ABC, abstractmethod

from injector import inject

from src.account.dto import UserAddDTO, UserDTO
from src.account.repository import UserRepository
from src.auth.services.hash_password import BaseHashPasswordService


class BaseUserService(ABC):
    def __init__(
        self,
        user_repository: UserRepository,
        hash_password_service: BaseHashPasswordService,
    ):
        self.user_repository = user_repository
        self.hash_password_service = hash_password_service

    @abstractmethod
    async def create_user(self, data: UserAddDTO) -> UserDTO: ...


class UserService(BaseUserService):
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        hash_password_service: BaseHashPasswordService,
    ):
        super().__init__(
            user_repository=user_repository,
            hash_password_service=hash_password_service,
        )

    async def create_user(self, data: UserAddDTO) -> UserDTO:
        hashed_password = self.hash_password_service.get_password_hash(
            password=data.password,
        )
        data_dict = data.model_dump(exclude={"password"})
        data_dict["hashed_password"] = hashed_password

        user = await self.user_repository.create(data=data_dict)
        return user

    async def create_superuser(self, data: UserAddDTO) -> UserDTO:
        hashed_password = self.hash_password_service.get_password_hash(
            password=data.password,
        )
        data_dict = data.model_dump(exclude={"password"})
        data_dict["hashed_password"] = hashed_password
        data_dict["is_superuser"] = True

        user = await self.user_repository.create(data=data_dict)
        return user
