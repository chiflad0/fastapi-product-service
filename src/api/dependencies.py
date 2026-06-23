from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.subcategory import SubcategoryService
from src.services.category import CategoryService
from src.database import get_session
from src.utils.pagination import PaginationParams


AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]

def get_category_service(session: AsyncSessionDep) -> CategoryService:
    return CategoryService(session)

def get_subcategory_service(session: AsyncSessionDep) -> SubcategoryService:
    return SubcategoryService(session)

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
SubcategoryServiceDep = Annotated[SubcategoryService, Depends(get_subcategory_service)]