from datetime import datetime, timezone

from database.session import SessionLocal

from models.news_article import (
    NewsArticle,
)

from repositories.news_article_repository import (
    NewsArticleRepository,
)


class NewsPersistenceService:

    @staticmethod
    def save_article(
        symbol: str,
        article_data: dict
    ):

        db = SessionLocal()

        try:

            repository = (
                NewsArticleRepository(db)
            )
            
            if repository.exists_by_provider_article_id(
                provider=article_data.get(
                    "provider",
                    ""
                ),
                provider_article_id=article_data.get(
                    "provider_article_id",
                    ""
                )
            ):
                return None

            entity = NewsArticle(
                symbol=symbol,
                title=article_data.get(
                    "title",
                    article_data.get(
                        "headline",
                        ""
                    )
                ),
                source=article_data.get(
                    "source",
                    "Unknown"
                ),
                
                provider=article_data.get(
                    "provider",
                    "unknown"
                ),
                                
                provider_article_id=
                    article_data.get(
                        "provider_article_id",
                        ""
                    ),
                published_at=article_data.get(
                    "published_at",
                    datetime.now(timezone.utc)
                ),
                sentiment=article_data[
                    "sentiment"
                ],
                confidence=article_data[
                    "confidence"
                ],
                events=",".join(
                    article_data.get(
                        "events",
                        []
                    )
                ),
                news_score=article_data[
                    "news_score"
                ],
                url="",
                content=article_data.get(
                    "content",
                    article_data.get(
                        "headline",
                        ""
                    )
                )
            )

            return repository.save(
                entity
            )

        finally:
            db.close()