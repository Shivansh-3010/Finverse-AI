from datetime import datetime

from historical_news.models.historical_news_record import (
    HistoricalNewsRecord,
)
from historical_news.normalization.news_normalizer import (
    NewsNormalizer,
)
from historical_news.normalization.deduplicator import (
    NewsDeduplicator,
)


def test_deduplicator():

    r1 = HistoricalNewsRecord(
        date=datetime(2024, 1, 1),
        title="Reliance reports earnings",
        source="a",
    )

    r2 = HistoricalNewsRecord(
        date=datetime(2024, 1, 1),
        title="Reliance reports earnings",
        source="b",
    )

    r1 = NewsNormalizer.normalize(r1)
    r2 = NewsNormalizer.normalize(r2)

    records = [r1, r2]

    unique_records = NewsDeduplicator.deduplicate(
        records
    )

    assert len(unique_records) == 1