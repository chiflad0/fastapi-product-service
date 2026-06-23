from uuid import UUID

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.models.mixins import *
from src.models.base import Base


class Subcategory(IDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "subcategories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_id: Mapped[UUID] = mapped_column(PG_UUID, ForeignKey("categories.id"))

    # Relationships
    parent: Mapped["Category"] = relationship(
        "Category",
        back_populates="subcategories"
    )
