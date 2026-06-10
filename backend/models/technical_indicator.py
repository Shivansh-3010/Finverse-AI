from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

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

    rsi: Mapped[float] = mapped_column(Float)
    mfi: Mapped[float] = mapped_column(Float)

    sma_20: Mapped[float] = mapped_column(Float)
    ema_20: Mapped[float] = mapped_column(Float)

    macd: Mapped[float] = mapped_column(Float)
    macd_signal: Mapped[float] = mapped_column(Float)

    adx: Mapped[float] = mapped_column(Float)

    atr: Mapped[float] = mapped_column(Float)

    obv: Mapped[float] = mapped_column(Float)
    vwap: Mapped[float] = mapped_column(Float)

    bb_upper: Mapped[float] = mapped_column(Float)
    bb_middle: Mapped[float] = mapped_column(Float)
    bb_lower: Mapped[float] = mapped_column(Float)