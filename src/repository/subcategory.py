from uuid import UUID

from sqlalchemy import select, func

from src.models import Subcategory
from src.repository.base import BaseRepository
from src.schema.subcategory import SubcategoryFilter


class SubcategoryRepository(BaseRepository[Subcategory]):
    async def get_subcategory_by_parent_id(
            self,
            parent_id: UUID,
            obj_filter: SubcategoryFilter | None = None,
            offset: int = 0,
            limit: int = 20
    ) -> list[Subcategory]:
        query = select(self.model).where(self.model.parent_id == parent_id).offset(offset).limit(limit)

        if obj_filter:
            query = obj_filter.filter(query)
            query = obj_filter.sort(query)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_subcategories_by_parent_id(self, parent_id: UUID) -> int:
        query = select(func.count()).select_from(self.model).where(self.model.parent_id == parent_id)
        result = await self.session.execute(query)
        return result.scalar_one()