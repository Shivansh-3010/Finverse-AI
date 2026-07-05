from datetime import datetime

from historical_news.models.historical_news_record import (
    HistoricalNewsRecord,
)
from historical_news.normalization.news_normalizer import (
    NewsNormalizer,
)


def test_generate_hash():

    record = HistoricalNewsRecord(
        date=datetime(2024, 1, 1),
        title="Reliance reports strong earnings",
        source="test",
    )

    normalized = NewsNormalizer.normalize(
        record
    )

    assert normalized.news_hash is not None

    assert len(normalized.news_hash) == 32