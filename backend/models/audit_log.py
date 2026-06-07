from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )
    action: Mapped[str] = mapped_column(String(255))
    metadata_json: Mapped[dict] = mapped_column(JSON)