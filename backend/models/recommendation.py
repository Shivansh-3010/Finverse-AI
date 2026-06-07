from sqlalchemy import Float, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    recommendation: Mapped[str] = mapped_column(String(20))
    confidence: Mapped[float] = mapped_column(Float)
    risk_score: Mapped[float] = mapped_column(Float)
    explanation: Mapped[dict] = mapped_column(JSON)