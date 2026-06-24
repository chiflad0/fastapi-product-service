from typing import TypeVar, Generic, Type

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select, func, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


ModelType = TypeVar("ModelType", bound=DeclarativeBase)
FilterType = TypeVar("FilterType", bound=Filter)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self, obj_filter: FilterType | None = None, offset: int = 0, limit: int = 20) -> list[ModelType]:
        query = select(self.model).offset(offset).limit(limit)

        if obj_filter:
            query = obj_filter.filter(query)
            query = obj_filter.sort(query)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def count(self, obj_filter: FilterType | None = None) -> int:
        query = select(func.count()).select_from(self.model)

        if obj_filter:
            query = obj_filter.filter(query)

        result = await self.session.execute(query)
        return result.scalar_one()

    async def get_by_id(self, obj_id: UUID) -> ModelType | None:
        result = await self.session.get(self.model, obj_id)
        return result

    async def add(self, obj_value: ModelType) -> ModelType:
        self.session.add(obj_value)
        await self.session.flush()
        return obj_value

    async def delete(self, obj_value: ModelType) -> None:
        await obj_value.soft_delete()

    async def restore(self, obj_value: ModelType) -> None:
        await obj_value.restore()
