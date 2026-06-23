from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.utils.pagination import PaginatedResponse


class CategoryResponse(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=5000)
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedCategoryResponse(PaginatedResponse[CategoryResponse]):
    pass


class CreateCategory(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Название категории")
    description: Optional[str] = Field(None, max_length=5000, description="Описание категории")


class UpdateCategory(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=5000)
