from uuid import UUID

from sqlalchemy import select, func

from src.models import Subcategory
from src.repository.base import BaseRepository


class SubcategoryRepository(BaseRepository[Subcategory]):
    async def get_subcategory_by_parent_id(
            self,
            parent_id: UUID,
            offset: int,
            limit: int
    ) -> list[Subcategory]:
        query = select(self.model).where(self.model.parent_id == parent_id).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_subcategories_by_parent_id(self, parent_id: UUID) -> int:
        query = select(func.count()).select_from(self.model).where(self.model.parent_id == parent_id)
        result = await self.session.execute(query)
        return result.scalar_one()