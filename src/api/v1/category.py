from fastapi import APIRouter, status, HTTPException
from uuid import UUID

from src.exceptions import ItemNotFoundException
from src.api.dependencies import PaginationDep, CategoryServiceDep, SubcategoryServiceDep
from src.schema.category import PaginatedCategoryResponse, CategoryResponse, CreateCategory, UpdateCategory
from src.schema.subcategory import PaginatedSubcategoryResponse


router = APIRouter(prefix="/category", tags=["Category"])


@router.get("/")
async def read_categories(
        pagination: PaginationDep,
        category_service: CategoryServiceDep
) -> PaginatedCategoryResponse:
    return await category_service.list_categories(pagination.page, pagination.size)


@router.get("/{id}")
async def read_category(
        category_id: UUID,
        category_service: CategoryServiceDep
) -> CategoryResponse:
    try:
        return await category_service.get_category_by_id(category_id)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{id}/subcategories")
async def read_subcategories(
        category_id: UUID,
        pagination: PaginationDep,
        subcategory_service: SubcategoryServiceDep
) -> PaginatedSubcategoryResponse:
    return await subcategory_service.get_subcategory_by_parent_id(category_id, pagination.page, pagination.size)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
        val: CreateCategory,
        category_service: CategoryServiceDep
) -> CategoryResponse:
    return await category_service.create_category(val)


@router.patch("/{id}")
async def update_category(
        category_id: UUID,
        payload: UpdateCategory,
        category_service: CategoryServiceDep
) -> CategoryResponse:
    try:
        return await category_service.update_category(category_id, payload)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: UUID,
        category_service: CategoryServiceDep
) -> None:
    try:
        await category_service.delete_category(category_id)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
