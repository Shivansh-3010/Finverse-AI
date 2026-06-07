from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin
from models.mixins.postgres import JSONB


class Recommendation(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "recommendations"

    symbol: Mapped[str] = mapped_column(String(20), index=True)
    recommendation: Mapped[str] = mapped_column(String(20))
    confidence: Mapped[float] = mapped_column(Float)
    risk_score: Mapped[float] = mapped_column(Float)
    explanation: Mapped[dict] = mapped_column(JSONB)