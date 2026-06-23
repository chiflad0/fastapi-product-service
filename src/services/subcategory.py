from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schema.subcategory import PaginatedSubcategoryResponse, SubcategoryResponse
from src.models import Subcategory
from src.repository.subcategory import SubcategoryRepository


class SubcategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.subcategory_repository = SubcategoryRepository(Subcategory, session)

    async def get_subcategory_by_parent_id(
        self,
        parent_id: UUID,
        page: int,
        size: int
    ) -> PaginatedSubcategoryResponse:
        offset = (page - 1) * size
        subcategories = await self.subcategory_repository.get_subcategory_by_parent_id(parent_id, offset, size)
        total = await self.subcategory_repository.count_subcategories_by_parent_id(parent_id)
        return PaginatedSubcategoryResponse(
            items=[SubcategoryResponse.model_validate(subcategory) for subcategory in subcategories],
            page=page,
            size=size,
            total=total
        )
