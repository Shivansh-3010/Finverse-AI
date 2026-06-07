from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin
from models.mixins.postgres import JSONB, UUID


class AuditLog(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "audit_logs"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )

    action: Mapped[str] = mapped_column(String(255))
    metadata_json: Mapped[dict] = mapped_column(JSONB)