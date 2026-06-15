from feature_store.news.news_embeddings import (
    NewsEmbeddings,
)
from metrics.monitoring_metrics import (
    MonitoringMetrics,
)


class NewsEmbeddingService:

    def __init__(self):

        self.store = (
            NewsEmbeddings()
        )

    def store_article(
        self,
        article: dict
    ):

        article_id = str(
            article.get(
                "provider_article_id",
                article.get(
                    "title",
                    "unknown"
                )
            )
        )

        metadata = {
            "symbol":
                article.get(
                    "symbol"
                ),

            "sentiment":
                article.get(
                    "sentiment"
                ),

            "news_score":
                article.get(
                    "news_score"
                ),
        }

        self.store.add_news(
            news_id=article_id,
            headline=article.get(
                "title",
                ""
            ),
            metadata=metadata,
        )
        
        MonitoringMetrics.increment_embeddings_created()
        