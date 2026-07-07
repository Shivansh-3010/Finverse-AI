from datetime import datetime

from sqlalchemy import DateTime, Float, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class RiskMetric(Base):
    __tablename__ = "risk_metrics"

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

    volatility_252d: Mapped[float] = mapped_column(
        Float
    )

    volatility_504d: Mapped[float] = mapped_column(
        Float
    )

    drawdown_252d: Mapped[float] = mapped_column(
        Float
    )

    drawdown_504d: Mapped[float] = mapped_column(
        Float
    )

    var95_252d: Mapped[float] = mapped_column(
        Float
    )

    var95_504d: Mapped[float] = mapped_column(
        Float
    )

    expected_shortfall_252d: Mapped[float] = mapped_column(
        Float
    )

    expected_shortfall_504d: Mapped[float] = mapped_column(
        Float
    )

    risk_score: Mapped[int] = mapped_column(
        Integer
    )
    
    risk_category: Mapped[str] = mapped_column(
        String(30)
    )