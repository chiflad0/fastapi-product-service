from fastapi import APIRouter, status, HTTPException
from uuid import UUID

from src.exceptions import ItemNotFoundException
from src.api.dependencies import PaginationDep, CategoryServiceDep, SubcategoryServiceDep, CategoryFilterDep
from src.schema.subcategory import PaginatedSubcategoryResponse, SubcategoryFilter
from src.schema.category import (
    PaginatedCategoryResponse,
    CategoryResponse,
    CreateCategory,
    UpdateCategory
)


router = APIRouter(prefix="/category", tags=["Category"])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedCategoryResponse,
    description="Получение списка категорий с фильтрацией и пагинацией."
)
async def get_all_categories(
        category_filter: CategoryFilterDep,
        pagination: PaginationDep,
        category_service: CategoryServiceDep
) -> PaginatedCategoryResponse:
    return await category_service.list_categories(category_filter, pagination)


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
    description="Получение информации о категории по ее ID."
)
async def get_category(
        category_id: UUID,
        category_service: CategoryServiceDep
) -> CategoryResponse:
    try:
        return await category_service.get_category_by_id(category_id)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    path="/{id}/subcategories",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedSubcategoryResponse,
    description="Получение списка подкатегорий, принадлежащих конкретной категории"
)
async def get_subcategories(
        category_id: UUID,
        subcategory_filter: SubcategoryFilter,
        pagination: PaginationDep,
        subcategory_service: SubcategoryServiceDep
) -> PaginatedSubcategoryResponse:
    try:
        return await subcategory_service.get_subcategory_by_parent_id(
            subcategory_filter,
            category_id,
            pagination.page,
            pagination.size
        )
    except ItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse,
    description="Создание новой категории"
)
async def add_category(
        val: CreateCategory,
        category_service: CategoryServiceDep
) -> CategoryResponse:
    return await category_service.create_category(val)


@router.patch(
    path="/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CategoryResponse,
    description="Обновление существующей категории"
)
async def update_category(
        category_id: UUID,
        payload: UpdateCategory,
        category_service: CategoryServiceDep
) -> CategoryResponse:
    try:
        return await category_service.update_category(category_id, payload)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление категории (мягкое удаление)"
)
async def delete_category(
        category_id: UUID,
        category_service: CategoryServiceDep
) -> None:
    try:
        await category_service.delete_category(category_id)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch(
    path="/{id}/restore",
    status_code=status.HTTP_202_ACCEPTED,
    description="Восстановление категории",
    response_model=CategoryResponse
)
async def restore_category(
        category_id: UUID,
        category_service: CategoryServiceDep
) -> CategoryResponse:
    try:
        return await category_service.restore_category(category_id)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
