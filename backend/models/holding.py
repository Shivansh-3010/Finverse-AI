from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Holding(Base):
    __tablename__ = "holdings"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    portfolio_id: Mapped[str] = mapped_column(
        ForeignKey("portfolios.id"),
        index=True
    )
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    quantity: Mapped[float] = mapped_column(Numeric(15, 4))
    avg_price: Mapped[float] = mapped_column(Numeric(15, 2))
    current_price: Mapped[float] = mapped_column(Numeric(15, 2))
    market_value: Mapped[float] = mapped_column(Numeric(15, 2))