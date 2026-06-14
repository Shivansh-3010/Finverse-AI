from services.news_collection_service import (
    NewsCollectionService
)

from services.news_persistence_service import (
    NewsPersistenceService
)


class NewsIngestionService:

    def __init__(self):

        self.collection = (
            NewsCollectionService()
        )

    def ingest_news(
        self,
        symbol: str
    ):

        articles = (
            self.collection
            .get_company_news_combined(
                symbol
            )
        )

        stored_count = 0

        for article in articles:

            saved = (
                NewsPersistenceService
                .save_article(
                    symbol=symbol,
                    article_data=article
                )
            )

            if saved:
                stored_count += 1

        return {
            "fetched": len(
                articles
            ),
            "stored": stored_count
        }