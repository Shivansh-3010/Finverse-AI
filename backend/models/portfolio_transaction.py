from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.postgres import UUID
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    SPLIT = "SPLIT"
    BONUS = "BONUS"


class PortfolioTransaction(
    UUIDMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "portfolio_transactions"

    portfolio_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("portfolios.id"),
        index=True,
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
        index=True,
    )

    transaction_type: Mapped[str] = mapped_column(
        String(20),
        index=True,
    )

    quantity: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 4),
        nullable=True,
    )

    price: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )