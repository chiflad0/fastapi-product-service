from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ItemNotFoundException
from src.schema.subcategory import PaginatedSubcategoryResponse, SubcategoryResponse, SubcategoryFilter
from src.models import Subcategory
from src.repository.subcategory import SubcategoryRepository
from src.utils.pagination import PaginationParams


class SubcategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.subcategory_repository = SubcategoryRepository(Subcategory, session)

    async def get_subcategory_by_parent_id(
            self,
            subcategory_filter: SubcategoryFilter,
            parent_id: UUID,
            page: int,
            size: int
    ) -> PaginatedSubcategoryResponse:
        offset = (page - 1) * size
        subcategories = await self.subcategory_repository.get_subcategory_by_parent_id(parent_id, subcategory_filter, offset, size)
        if not subcategories:
            raise ItemNotFoundException(parent_id)

        total = await self.subcategory_repository.count_subcategories_by_parent_id(parent_id)
        return PaginatedSubcategoryResponse(
            items=[SubcategoryResponse.model_validate(subcategory) for subcategory in subcategories],
            page=page,
            size=size,
            total=total
        )

    async def list_subcategories(
            self,
            subcategory_filter: SubcategoryFilter,
            pagination: PaginationParams
    ) -> PaginatedSubcategoryResponse:
        offset = (pagination.page - 1) * pagination.size
        categories = await self.subcategory_repository.get_all(subcategory_filter, offset, pagination.size)
        total = await self.subcategory_repository.count(subcategory_filter)
        return PaginatedSubcategoryResponse(
            items=[SubcategoryResponse.model_validate(category) for category in categories],
            page=pagination.page,
            size=pagination.size,
            total=total
        )