from sqlalchemy import Float, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class AgentOutput(Base):
    __tablename__ = "agent_outputs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    agent_name: Mapped[str] = mapped_column(String(100))
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    output: Mapped[dict] = mapped_column(JSON)
    execution_time: Mapped[float] = mapped_column(Float)