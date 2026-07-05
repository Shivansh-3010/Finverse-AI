from historical_news.pipeline.backfill_pipeline import (
    HistoricalNewsBackfillPipeline,
)


def test_backfill_pipeline():

    pipeline = HistoricalNewsBackfillPipeline()

    records = pipeline.load_all()

    assert len(records) > 500000