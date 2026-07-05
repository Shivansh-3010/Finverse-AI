from datetime import datetime

from historical_news.models.historical_news_record import (
    HistoricalNewsRecord,
)


def test_historical_news_record_creation():
    record = HistoricalNewsRecord(
        date=datetime(2020, 5, 26),
        title="Test Headline",
        description="Test Description",
        source="indian_financial_news",
    )

    assert record.title == "Test Headline"
    assert record.source == "indian_financial_news"