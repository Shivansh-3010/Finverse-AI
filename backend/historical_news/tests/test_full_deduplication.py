from historical_news.pipeline.backfill_pipeline import (
    HistoricalNewsBackfillPipeline,
)
from historical_news.normalization.news_normalizer import (
    NewsNormalizer,
)
from historical_news.normalization.deduplicator import (
    NewsDeduplicator,
)


def test_full_deduplication():

    pipeline = HistoricalNewsBackfillPipeline()

    records = pipeline.load_all()

    print(f"\nRaw records: {len(records):,}")

    normalized_records = [
        NewsNormalizer.normalize(record)
        for record in records
    ]

    unique_records = NewsDeduplicator.deduplicate(
        normalized_records
    )

    print(f"Unique records: {len(unique_records):,}")

    duplicates = len(records) - len(unique_records)

    print(f"Duplicates removed: {duplicates:,}")

    duplicate_pct = (
        duplicates / len(records)
    ) * 100

    print(
        f"Duplicate percentage: "
        f"{duplicate_pct:.2f}%"
    )

    assert len(unique_records) > 400000