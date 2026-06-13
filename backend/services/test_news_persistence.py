from services.news_persistence_service import (
    NewsPersistenceService
)

result = (
    NewsPersistenceService.save_article(
        symbol="RELIANCE",
        article_data={
            "headline":
                "Reliance Industries reports strong quarterly earnings growth",

            "source":
                "Finnhub",

            "provider":
                "finnhub",

            "provider_article_id":
                "test-001",

            "sentiment":
                "positive",

            "confidence":
                0.95,

            "events":
                [
                    "earnings"
                ],

            "news_score":
                89,
        }
    )
)

print(result)