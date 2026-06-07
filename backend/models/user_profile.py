from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin
from models.mixins.postgres import UUID


class UserProfile(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )

    risk_tolerance: Mapped[str] = mapped_column(String(50))
    investment_goal: Mapped[str] = mapped_column(String(100))
    investment_horizon: Mapped[str] = mapped_column(String(50))
    annual_income: Mapped[float] = mapped_column(Numeric(15, 2))