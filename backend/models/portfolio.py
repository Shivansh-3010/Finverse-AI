from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin
from models.mixins.postgres import UUID


class Portfolio(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "portfolios"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )

    name: Mapped[str] = mapped_column(String(255))
    total_value: Mapped[float] = mapped_column(Numeric(15, 2))