from typing import Generic, TypeVar
from pydantic import BaseModel, Field, computed_field


T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Номер страницы")
    size: int = Field(20, gt=0, le=100, description="Количество элементов на странице")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] = Field(description="Список запрошенных элементов")
    page: int = Field(1, ge=1, description="Текущая страница")
    size: int = Field(20, ge=1, le=100, description="Размер страницы")
    total: int = Field(ge=0, description="Общее количество элементов во всей базе")

    @computed_field
    @property
    def pages(self) -> int:
        """Общее количество страниц"""
        if self.total == 0:
            return 0
        return (self.total + self.size - 1) // self.size

    @computed_field
    @property
    def has_next(self) -> bool:
        """Есть ли следующая страница"""
        return self.page < self.pages

    @computed_field
    @property
    def has_previous(self) -> bool:
        """Есть ли предыдущая страница"""
        return self.page > 1