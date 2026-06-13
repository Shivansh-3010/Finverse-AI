from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class SupportResistance(Base):
    __tablename__ = "support_resistance"

    symbol: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    timeframe: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True
    )

    nearest_support: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    nearest_resistance: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    signal_level: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    signal: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )