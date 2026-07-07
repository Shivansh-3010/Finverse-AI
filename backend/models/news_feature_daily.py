from datetime import date

from sqlalchemy import (
    Date,
    Float,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from models.base import Base


class NewsFeatureDaily(Base):
    __tablename__ = "news_features_daily"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    date: Mapped[date] = mapped_column(
        Date
    )

    symbol: Mapped[str] = mapped_column(
        String(20)
    )

    news_count: Mapped[int] = mapped_column(
        Integer
    )

    positive_count: Mapped[int] = mapped_column(
        Integer
    )

    negative_count: Mapped[int] = mapped_column(
        Integer
    )

    neutral_count: Mapped[int] = mapped_column(
        Integer
    )

    positive_ratio: Mapped[float] = mapped_column(
        Float
    )

    negative_ratio: Mapped[float] = mapped_column(
        Float
    )

    avg_confidence: Mapped[float] = mapped_column(
        Float
    )

    positive_confidence_mean: Mapped[float] = mapped_column(
        Float
    )

    negative_confidence_mean: Mapped[float] = mapped_column(
        Float
    )

    neutral_confidence_mean: Mapped[float] = mapped_column(
        Float
    )

    sentiment_score: Mapped[float] = mapped_column(
        Float
    )

    earnings_count: Mapped[int] = mapped_column(
        Integer
    )

    funding_count: Mapped[int] = mapped_column(
        Integer
    )

    regulatory_count: Mapped[int] = mapped_column(
        Integer
    )

    macro_count: Mapped[int] = mapped_column(
        Integer
    )

    mergers_acquisitions_count: Mapped[int] = mapped_column(
        Integer
    )

    event_score: Mapped[float] = mapped_column(
        Float
    )

    sentiment_momentum: Mapped[float] = mapped_column(
        Float
    )

    event_intensity: Mapped[float] = mapped_column(
        Float
    )

    positive_confidence: Mapped[float] = mapped_column(
        Float
    )

    negative_confidence: Mapped[float] = mapped_column(
        Float
    )

    neutral_confidence: Mapped[float] = mapped_column(
        Float
    )

    event_article_ratio: Mapped[float] = mapped_column(
        Float
    )

    dominant_sentiment: Mapped[str] = mapped_column(
        String(20)
    )

    has_earnings_event: Mapped[int] = mapped_column(
        Integer
    )

    has_regulatory_event: Mapped[int] = mapped_column(
        Integer
    )

    has_funding_event: Mapped[int] = mapped_column(
        Integer
    )

    has_ma_event: Mapped[int] = mapped_column(
        Integer
    )

    news_count_3d: Mapped[float] = mapped_column(
        Float
    )

    sentiment_score_3d: Mapped[float] = mapped_column(
        Float
    )

    event_score_3d: Mapped[float] = mapped_column(
        Float
    )

    news_count_7d: Mapped[float] = mapped_column(
        Float
    )

    sentiment_score_7d: Mapped[float] = mapped_column(
        Float
    )

    event_score_7d: Mapped[float] = mapped_column(
        Float
    )

    rolling_news_momentum: Mapped[float] = mapped_column(
        Float
    )

    news_attention_score: Mapped[float] = mapped_column(
        Float
    )