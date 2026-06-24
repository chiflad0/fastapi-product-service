from uuid import UUID

from fastapi import APIRouter, status, HTTPException
from fastapi import APIRouter

from src.api.dependencies import PaginationDep, SubcategoryServiceDep, SubcategoryFilterDep
from src.schema.subcategory import PaginatedSubcategoryResponse, SubcategoryResponse, CreateSubcategory, UpdateSubcategory


router = APIRouter(prefix="/subcategory", tags=["Subcategory"])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedSubcategoryResponse,
    description="Получение списка подкатегорий с фильтрацией и пагинацией."
)
async def get_all_categories(
        subcategory_filter: SubcategoryFilterDep,
        pagination: PaginationDep,
        subcategory_service: SubcategoryServiceDep
) -> PaginatedSubcategoryResponse:
    return await subcategory_service.list_subcategories(subcategory_filter, pagination)


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    response_model=SubcategoryResponse,
    description="Получение информации о подкатегории по ее ID."
)
async def get_category(
        category_id: UUID,
        category_service: SubcategoryServiceDep
) -> SubcategoryResponse:
    pass


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=SubcategoryResponse,
    description="Создание новой подкатегории"
)
async def add_category(
        val: CreateSubcategory,
        category_service: SubcategoryServiceDep
) -> SubcategoryResponse:
    pass


@router.patch(
    path="/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=SubcategoryResponse,
    description="Обновление существующей подкатегории"
)
async def update_category(
        category_id: UUID,
        payload: UpdateSubcategory,
        category_service: SubcategoryServiceDep
) -> SubcategoryResponse:
    pass


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление подкатегории (мягкое удаление)"
)
async def delete_category(
        category_id: UUID,
        category_service: SubcategoryServiceDep
) -> None:
    pass


@router.patch(
    path="/{id}/restore",
    status_code=status.HTTP_202_ACCEPTED,
    description="Восстановление подкатегории",
    response_model=SubcategoryResponse
)
async def restore_category(
        category_id: UUID,
        category_service: SubcategoryServiceDep
) -> SubcategoryResponse:
    pass