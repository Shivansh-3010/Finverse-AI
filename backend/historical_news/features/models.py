from dataclasses import dataclass


@dataclass
class DailyNewsFeature:

    date: str

    symbol: str

    # Volume
    news_count: int

    # Sentiment Counts
    positive_count: int
    negative_count: int
    neutral_count: int

    # Sentiment Ratios
    positive_ratio: float
    negative_ratio: float

    # Confidence
    avg_confidence: float

    # Aggregate Sentiment
    sentiment_score: float

    # Event Counts
    earnings_count: int
    funding_count: int
    regulatory_count: int
    macro_count: int
    mergers_acquisitions_count: int
    
    # Event Impact
    event_score: float