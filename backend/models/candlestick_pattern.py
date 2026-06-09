from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class CandlestickPattern(Base):
    __tablename__ = "candlestick_patterns"

    symbol: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True
    )

    pattern_name: Mapped[str] = mapped_column(
        String(100)
    )

    signal: Mapped[str] = mapped_column(
        String(20)
    )

    strength: Mapped[float] = mapped_column(
        Float
    )

    candlestick_score: Mapped[float] = mapped_column(
        Float
    )