from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.news_article import (
    NewsArticle,
)


class NewsArticleRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def get_latest(
        self,
        symbol: str
    ):
        return (
            self.db.query(NewsArticle)
            .filter(
                NewsArticle.symbol == symbol
            )
            .order_by(
                desc(
                    NewsArticle.published_at
                )
            )
            .first()
        )

    def get_history(
        self,
        symbol: str
    ):
        return (
            self.db.query(NewsArticle)
            .filter(
                NewsArticle.symbol == symbol
            )
            .order_by(
                NewsArticle.published_at
            )
            .all()
        )

    def save(
        self,
        article: NewsArticle
    ):
        saved_article = (
            self.db.merge(article)
        )

        self.db.commit()

        self.db.refresh(
            saved_article
        )

        return saved_article
    
    def exists_by_provider_article(
        self,
        provider: str,
        provider_article_id: str
    ):

        return (
            self.db.query(
                NewsArticle
            )
            .filter(
                NewsArticle.provider
                == provider,

                NewsArticle
                .provider_article_id
                == provider_article_id
            )
            .first()
            is not None
        )
        
    def exists_by_provider_article_id(
        self,
        provider: str,
        provider_article_id: str
    ):

        return (
            self.db.query(
                NewsArticle
            )
            .filter(
                NewsArticle.provider ==
                    provider,

                NewsArticle.provider_article_id ==
                    provider_article_id
            )
            .first()
            is not None
        )