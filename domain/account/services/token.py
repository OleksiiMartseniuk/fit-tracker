import uuid
from abc import ABC, abstractmethod

from injector import inject

from domain.account.repository import TokeDjangoRepository


class BaseTokeService(ABC):
    def __init__(self, token_repository: TokeDjangoRepository):
        self.token_repository = token_repository

    @abstractmethod
    def get_or_create_token(self, user_id: int) -> str:
        pass


class TokenService(BaseTokeService):
    @inject
    def __init__(self, token_repository: TokeDjangoRepository):
        super().__init__(token_repository)

    def get_or_create_token(self, user_id: int) -> str:
        token = self.token_repository.get_or_none(user_id=user_id)
        if token:
            return token.access_token

        token = self.token_repository.create(
            user_id=user_id,
            access_token=uuid.uuid4().hex,
        )
        return token.access_token
