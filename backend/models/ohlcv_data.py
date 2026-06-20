from sqlalchemy import String, Float, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class OHLCVData(Base):
    __tablename__ = "ohlcv_data"

    symbol: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )
    
    timeframe: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True
    )

    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)

    volume: Mapped[int] = mapped_column(BigInteger)
    
    dividend: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    stock_split: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )