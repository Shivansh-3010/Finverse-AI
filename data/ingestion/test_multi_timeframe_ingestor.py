from multi_timeframe_ingestor import (
    MultiTimeframeIngestor,
)

ingestor = MultiTimeframeIngestor()

rows = ingestor.ingest_and_store(
    "RELIANCE.NS"
)

print(
    f"Total rows inserted: {rows}"
)