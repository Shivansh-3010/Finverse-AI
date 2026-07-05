from pathlib import Path

import pandas as pd

from historical_news.pipeline.backfill_pipeline import (
    HistoricalNewsBackfillPipeline,
)
from historical_news.normalization.news_normalizer import (
    NewsNormalizer,
)
from historical_news.normalization.deduplicator import (
    NewsDeduplicator,
)


OUTPUT_FILE = (
    "../datasets/historical_news_processed/"
    "historical_news_v1.csv"
)


def export_historical_news():

    print("Loading records...")

    pipeline = HistoricalNewsBackfillPipeline()

    records = pipeline.load_all()

    print(f"Raw records: {len(records):,}")

    print("Generating hashes...")

    records = [
        NewsNormalizer.normalize(record)
        for record in records
    ]

    print("Removing duplicates...")

    records = NewsDeduplicator.deduplicate(records)

    print(f"Unique records: {len(records):,}")

    output_dir = Path(
        "../datasets/historical_news_processed"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = []

    for record in records:

        rows.append(
            {
                "date": record.date,
                "title": record.title,
                "description": record.description,
                "source": record.source,
                "news_hash": record.news_hash,
            }
        )

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(
        f"Saved {len(df):,} records "
        f"to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    export_historical_news()