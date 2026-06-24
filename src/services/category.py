from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ItemNotFoundException
from src.models.category import Category
from src.repository.category import CategoryRepository
from src.utils.pagination import PaginationParams
from src.schema.category import (
    PaginatedCategoryResponse,
    CategoryResponse,
    CreateCategory,
    UpdateCategory,
    CategoryFilter
)


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.category_repository = CategoryRepository(Category, session)

    async def list_categories(
            self,
            category_filter: CategoryFilter,
            pagination: PaginationParams
    ) -> PaginatedCategoryResponse:
        offset = (pagination.page - 1) * pagination.size
        categories = await self.category_repository.get_all(category_filter, offset, pagination.size)
        total = await self.category_repository.count(category_filter)
        return PaginatedCategoryResponse(
            items=[CategoryResponse.model_validate(category) for category in categories],
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    async def get_category_by_id(self, category_id: UUID) -> CategoryResponse:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise ItemNotFoundException(category_id)

        return CategoryResponse.model_validate(category)

    async def create_category(self, val: CreateCategory) -> CategoryResponse:
        category_orm = Category(name=val.name, description=val.description)
        new_category = await self.category_repository.add(category_orm)

        await self.session.commit()

        return CategoryResponse.model_validate(new_category)

    async def update_category(self, category_id: UUID, val: UpdateCategory) -> CategoryResponse:
        category_for_update = await self.category_repository.get_by_id(category_id)
        if not category_for_update:
            raise ItemNotFoundException(category_id)

        update_data = val.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category_for_update, field, value)

        await self.session.commit()

        return CategoryResponse.model_validate(category_for_update)


    async def delete_category(self, category_id: UUID) -> None:
        category_for_delete = await self.category_repository.get_by_id(category_id)
        if not category_for_delete:
            raise ItemNotFoundException(category_id)

        await self.category_repository.delete(category_for_delete)
        await self.session.commit()


    async def restore_category(self, category_id: UUID) -> CategoryResponse:
        category_for_restore = await self.category_repository.get_by_id(category_id)
        if not category_for_restore:
            raise ItemNotFoundException(category_id)

        await self.category_repository.restore(category_for_restore)

        await self.session.commit()
        await self.session.refresh(category_for_restore)

        return CategoryResponse.model_validate(category_for_restore)
