from services.news_ingestion_service import (
    NewsIngestionService
)

service = (
    NewsIngestionService()
)

result = (
    service.ingest_news(
        "AAPL"
    )
)

print(result)