from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from models.base import Base


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    symbol: Mapped[str] = mapped_column(
        String(20)
    )

    title: Mapped[str] = mapped_column(
        String(500)
    )

    source: Mapped[str] = mapped_column(
        String(100)
    )
    
    provider: Mapped[str] = (
        mapped_column(
            String(50)
        )
    )

    provider_article_id: Mapped[str] = (
        mapped_column(
            Text
        )
    )

    events: Mapped[str] = (
        mapped_column(
            Text
        )
    )

    published_at: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True)
        )
    )

    sentiment: Mapped[str] = (
        mapped_column(
            String(20)
        )
    )

    confidence: Mapped[float] = (
        mapped_column(Float)
    )

    news_score: Mapped[int] = (
        mapped_column(Integer)
    )

    url: Mapped[str] = mapped_column(
        String(1000)
    )

    content: Mapped[str] = (
        mapped_column(Text)
    )