from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from models.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

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

    model_name: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    prediction: Mapped[float] = mapped_column(
        Float
    )

    confidence: Mapped[float] = mapped_column(
        Float
    )

    horizon: Mapped[str] = mapped_column(
        String(20)
    )