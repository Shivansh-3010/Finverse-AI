from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin
from models.mixins.postgres import JSONB


class AgentOutput(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "agent_outputs"

    agent_name: Mapped[str] = mapped_column(String(100))
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    output: Mapped[dict] = mapped_column(JSONB)
    execution_time: Mapped[float] = mapped_column(Float)