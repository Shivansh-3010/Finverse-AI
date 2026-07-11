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
    
    distance_to_support_pct: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    distance_to_resistance_pct: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    support_strength: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    resistance_strength: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    breakout_zone_lower: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    breakout_zone_upper: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    breakdown_zone_lower: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    breakdown_zone_upper: Mapped[float | None] = mapped_column(
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
    
    distance_to_support_pct: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    distance_to_resistance_pct: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    support_strength: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    resistance_strength: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )