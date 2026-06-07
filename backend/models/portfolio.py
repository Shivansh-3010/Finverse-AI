from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    total_value: Mapped[float] = mapped_column(Numeric(15, 2))