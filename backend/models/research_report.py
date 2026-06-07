from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class ResearchReport(Base):
    __tablename__ = "research_reports"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    company: Mapped[str] = mapped_column(String(100), index=True)
    report_type: Mapped[str] = mapped_column(String(50))
    summary: Mapped[str] = mapped_column(Text)
    report_data: Mapped[dict] = mapped_column(JSON)