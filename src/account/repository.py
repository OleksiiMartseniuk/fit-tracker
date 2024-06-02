from injector import inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.dto import UserDTO
from src.account.models import User
from src.database.mixins import RepositoryCRUDMixin


class UserRepository(RepositoryCRUDMixin[UserDTO]):
    model = User
    read_dto = UserDTO

    @inject
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory
