import datetime
from enum import Enum

from sqlalchemy import Boolean, TIMESTAMP, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column


class DeleteReason(str, Enum):
    MANUAL = "manual" # Удалил пользователь
    CASCADE = "cascade" # Удалилось автоматически из-за родителя


class SoftDeleteMixin:
    """Mixin для реализации мягкого удаления (soft delete)."""
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    delete_reason: Mapped[DeleteReason | None] = mapped_column(SQLEnum(DeleteReason), nullable=True)

    async def soft_delete(self, reason: DeleteReason = DeleteReason.MANUAL):
        self.is_deleted = True
        self.deleted_at = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        self.delete_reason = reason

    async def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.delete_reason = None
