from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.models import Subcategory
from src.utils.pagination import PaginatedResponse


class SubcategoryResponse(BaseModel):
    id: UUID = Field(description="Уникальный идентификатор подкатегории")
    name: str = Field(min_length=1, max_length=100, description="Название подкатегории")
    description: Optional[str] = Field(None, max_length=5000, description="Описание подкатегории")
    is_deleted: bool = Field(description="Флаг мягкого удаления")
    created_at: datetime = Field(description="Дата и время создания записи")
    updated_at: datetime = Field(description="Дата и время последнего обновления записи")

    model_config = ConfigDict(from_attributes=True)


class PaginatedSubcategoryResponse(PaginatedResponse[SubcategoryResponse]):
    pass


class SubcategoryFilter(Filter):
    name__ilike: Optional[str] = Field(None, description="Поиск категории по названию (регистронезависимый, частичное совпадение)")
    is_deleted: Optional[bool] = Field(None, description="Фильтр по статусу удаления: true - только удаленные, false - только активные")
    order_by: list[str] = Field(default=["id"], description="Список полей для сортировки")

    class Constants(Filter.Constants):
        model = Subcategory


class CreateSubcategory(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Название подкатегории")
    description: Optional[str] = Field(None, max_length=5000, description="Описание подкатегории")


class UpdateSubcategory(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Название подкатегории")
    description: Optional[str] = Field(None, max_length=5000, description="Описание подкатегории")
