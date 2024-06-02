from abc import ABC, abstractmethod

from passlib.context import CryptContext


class BaseHashPasswordService(ABC):
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...

    @abstractmethod
    def get_password_hash(self, password: str) -> str: ...


class HashPasswordService(BaseHashPasswordService):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
