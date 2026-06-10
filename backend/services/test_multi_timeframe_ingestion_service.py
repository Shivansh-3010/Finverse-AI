from services.multi_timeframe_ingestion_service import (
    MultiTimeframeIngestionService,
)


service = (
    MultiTimeframeIngestionService()
)

print(
    service.ingest_symbol(
        "RELIANCE.NS"
    )
)