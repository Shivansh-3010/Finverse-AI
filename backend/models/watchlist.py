from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin
from models.mixins.postgres import UUID


class Watchlist(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "watchlists"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )

    symbol: Mapped[str] = mapped_column(String(20), index=True)