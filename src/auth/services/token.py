import uuid
from abc import ABC, abstractmethod

from injector import inject

from src.auth.dto import TokenDTO
from src.auth.repository import TokenRepository


class BaseTokenService(ABC):
    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository

    @abstractmethod
    async def get_or_create(self, user_id: int) -> TokenDTO: ...

    def generate_token(self) -> str: ...


class TokenService(BaseTokenService):
    @inject
    def __init__(self, token_repository: TokenRepository):
        super().__init__(token_repository=token_repository)

    async def get_or_create(self, user_id: int) -> TokenDTO:
        token = await self.token_repository.get_or_none(user_id=user_id)
        if token:
            return token

        token = await self.token_repository.create(
            data={
                "user_id": user_id,
                "token": self.generate_token(),
            }
        )
        return token

    def generate_token(self) -> str:
        return uuid.uuid4().hex
