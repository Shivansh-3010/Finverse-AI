from backend.services.news_collection_service import (
    NewsCollectionService,
)

service = NewsCollectionService()

result = (
    service.get_company_news_combined(
        "AAPL"
    )
)

print(
    f"Articles Found: {len(result)}"
)

if result:
    print(result[0])