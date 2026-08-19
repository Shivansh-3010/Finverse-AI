from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.postgres import UUID
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin


class PortfolioSnapshot(
    UUIDMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "portfolio_snapshots"

    portfolio_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("portfolios.id"),
        index=True,
    )

    snapshot_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    portfolio_value: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    cash: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    invested_value: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    return_value: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    risk_score: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 4),
        nullable=True,
    )