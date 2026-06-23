from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.models.mixins import *


class Category(IDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    subcategories: Mapped[list["Subcategory"]] = relationship(
        "Subcategory",
        back_populates="parent",
        cascade="save-update, merge"
    )
