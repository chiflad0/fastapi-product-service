from typing import Generic, TypeVar
from pydantic import BaseModel, Field, computed_field


T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(ge=1, default=1)
    size: int = Field(gt=0, le=100, default=20)


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int = Field(ge=1, default=1)
    size: int = Field(ge=1, le=100, default=20)
    total: int = Field(ge=0)

    @computed_field
    @property
    def pages(self) -> int:
        if self.total == 0:
            return 0
        return (self.total + self.size - 1) // self.size

    @computed_field
    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @computed_field
    @property
    def has_previous(self) -> bool:
        return self.page > 1