from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.engine import default

from src.utils.pagination import PaginatedResponse
from src.models.category import Category


class CategoryResponse(BaseModel):
    id: UUID = Field(description="Уникальный идентификатор категории")
    name: str = Field(min_length=1, max_length=100, description="Название категории")
    description: Optional[str] = Field(None, max_length=5000, description="Описание категории")
    is_deleted: bool = Field(description="Флаг мягкого удаления")
    created_at: datetime = Field(description="Дата и время создания записи")
    updated_at: datetime = Field(description="Дата и время последнего обновления записи")

    model_config = ConfigDict(from_attributes=True)


class PaginatedCategoryResponse(PaginatedResponse[CategoryResponse]):
    pass


class CategoryFilter(Filter):
    name__ilike: Optional[str] = Field(None, description="Поиск категории по названию (регистронезависимый, частичное совпадение)")
    is_deleted: Optional[bool] = Field(None, description="Фильтр по статусу удаления: true - только удаленные, false - только активные")
    order_by: list[str] = Field(default=["id"], description="Список полей для сортировки")

    class Constants(Filter.Constants):
        model = Category


class CreateCategory(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Название категории")
    description: Optional[str] = Field(None, max_length=5000, description="Описание категории")


class UpdateCategory(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Название категории")
    description: Optional[str] = Field(None, max_length=5000, description="Описание категории")
