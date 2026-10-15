from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.postgres import UUID
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin


class PortfolioGoal(UUIDMixin, TimestampMixin, Base):
    """A financial goal associated with a portfolio."""

    __tablename__ = "portfolio_goals"

    portfolio_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("portfolios.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    goal_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    target_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    current_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0.00",
    )

    monthly_contribution: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0.00",
    )

    target_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expected_annual_return_pct: Mapped[Decimal] = mapped_column(
        Numeric(6, 3),
        nullable=False,
        default=Decimal("7.000"),
        server_default="7.000",
    )
