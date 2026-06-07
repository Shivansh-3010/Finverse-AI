from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )
    risk_tolerance: Mapped[str] = mapped_column(String(50))
    investment_goal: Mapped[str] = mapped_column(String(100))
    investment_horizon: Mapped[str] = mapped_column(String(50))
    annual_income: Mapped[float] = mapped_column(Numeric(15, 2))