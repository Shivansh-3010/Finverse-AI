from feature_store.news.news_embeddings import (
    NewsEmbeddings,
)

store = NewsEmbeddings()

store.add_news(
    news_id="reliance_test_001",
    headline="Reliance Industries reports strong quarterly earnings growth",
    metadata={
        "symbol": "RELIANCE",
        "sentiment": "positive",
        "news_score": 89,
    }
)

result = store.search(
    "Reliance earnings"
)

print(result)