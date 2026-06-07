from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.mixins.timestamp import TimestampMixin
from models.mixins.uuid import UUIDMixin
from models.mixins.postgres import JSONB


class ResearchReport(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "research_reports"

    company: Mapped[str] = mapped_column(String(100), index=True)
    report_type: Mapped[str] = mapped_column(String(50))
    summary: Mapped[str] = mapped_column(Text)
    report_data: Mapped[dict] = mapped_column(JSONB)