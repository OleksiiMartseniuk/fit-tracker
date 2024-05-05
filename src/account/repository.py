from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.dto import UserAddDto, UserDto
from src.account.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self) -> UserDto:
        stmt = select(User)
        res = await self.session.execute(stmt)
        response_orm = res.scalars().one()
        return UserDto.model_validate(response_orm, from_attributes=True)

    async def add_user(self, user_dto: UserAddDto):
        user = User(**user_dto.model_dump())
        self.session.add(user)
        return user
