from typing import TypeVar, Generic, Type

from sqlalchemy import select, func, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self, offset: int = 0, limit: int = 20) -> list[ModelType]:
        query = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count(self) -> int:
        query = select(func.count(self.model.id))
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
        await self.session.delete(obj_value)