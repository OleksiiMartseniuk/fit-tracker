from injector import inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dto import TokenDTO
from src.auth.models import Token
from src.database.mixins import RepositoryCRUDMixin


class TokenRepository(RepositoryCRUDMixin[TokenDTO]):
    model = Token
    read_dto = TokenDTO

    @inject
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory
