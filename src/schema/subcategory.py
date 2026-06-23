from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.utils.pagination import PaginatedResponse


class SubcategoryResponse(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=5000)
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedSubcategoryResponse(PaginatedResponse[SubcategoryResponse]):
    pass

