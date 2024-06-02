from datetime import datetime
from typing import Generic, Optional, TypeVar

from sqlalchemy import delete, select, text, update
from sqlalchemy.orm import Mapped, mapped_column

ReadDTO = TypeVar("ReadDTO")


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=datetime.utcnow,
        nullable=True,
    )


class RepositoryCRUDMixin(Generic[ReadDTO]):
    """
    :param
    model: sqlalchemy model
    read_dto: pydantic model
    """

    async def create(self, data: dict) -> ReadDTO:
        async with self.session_factory() as session:
            obj = self.model(**data)
            session.add(obj)
            await session.commit()
            return self.read_dto.model_validate(obj, from_attributes=True)

    async def get(self, **kwargs) -> ReadDTO:
        async with self.session_factory() as session:
            stmt = select(self.model).filter_by(**kwargs)
            result = await session.execute(stmt)
            obj = result.scalars().one()
            return self.read_dto.model_validate(obj, from_attributes=True)

    async def get_or_none(self, **kwargs) -> ReadDTO | None:
        async with self.session_factory() as session:
            stmt = select(self.model).filter_by(**kwargs)
            result = await session.execute(stmt)
            obj = result.scalars().one_or_none()
            if obj is None:
                return None
            return self.read_dto.model_validate(obj, from_attributes=True)

    async def update(self, data: dict, **kwargs) -> None:
        async with self.session_factory() as session:
            stmt = update(self.model).filter_by(**kwargs).values(data)
            await session.execute(stmt)
            await session.commit()

    async def delete(self, **kwargs) -> None:
        async with self.session_factory() as session:
            stmt = delete(self.model).filter_by(**kwargs)
            await session.execute(stmt)
            await session.commit()
