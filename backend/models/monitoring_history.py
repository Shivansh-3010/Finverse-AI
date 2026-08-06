from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from models.base import Base


class MonitoringHistory(Base):

    __tablename__ = "monitoring_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    model_name: Mapped[str] = mapped_column(
        String(50),
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
    )

    horizon: Mapped[str] = mapped_column(
        String(20),
    )

    status: Mapped[str] = mapped_column(
        String(20),
    )

    feature_drift: Mapped[bool] = mapped_column(
        Boolean,
    )

    prediction_drift: Mapped[bool] = mapped_column(
        Boolean,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
    )

    recommendation: Mapped[str] = mapped_column(
        String(100),
    )

    mae: Mapped[float] = mapped_column(
        Float,
    )

    rmse: Mapped[float] = mapped_column(
        Float,
    )

    mape: Mapped[float] = mapped_column(
        Float,
    )

    directional_accuracy: Mapped[float] = mapped_column(
        Float,
    )