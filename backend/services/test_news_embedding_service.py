from services.news_embedding_service import (
    NewsEmbeddingService,
)

service = (
    NewsEmbeddingService()
)

service.store_article(
    {
        "provider_article_id":
            "test_001",

        "title":
            "Reliance Industries reports strong quarterly earnings growth",

        "symbol":
            "RELIANCE",

        "sentiment":
            "positive",

        "news_score":
            89,
    }
)

print(
    "Stored successfully"
)