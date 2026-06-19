from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.news_article import (
    NewsArticle,
)
from datetime import datetime, timedelta, timezone


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
        
    def get_recent_summary(
        self,
        symbol: str,
        limit: int = 20
    ):

        articles = (
            self.db.query(
                NewsArticle
            )
            .filter(
                NewsArticle.symbol == symbol
            )
            .order_by(
                desc(
                    NewsArticle.published_at
                )
            )
            .limit(limit)
            .all()
        )
        
        recent_cutoff = (
            datetime.now(timezone.utc)
            - timedelta(days=1)
        )

        recent_articles = [

            article

            for article in articles

            if (
                article.published_at
                and
                article.published_at >= recent_cutoff
            )
        ]

        if not articles:

            return {
                "avg_news_score": 0.0,
                "avg_confidence": 0.0,
                "article_count": 0,
            }

        return {

            "avg_news_score":
                sum(
                    article.news_score
                    or 0
                    for article in articles
                )
                / len(articles),

            "avg_confidence":
                sum(
                    article.confidence
                    or 0
                    for article in articles
                )
                / len(articles),

            "article_count":
                len(articles),
                
            "recent_article_count":
                len(
                    recent_articles
                ),

            "positive_count":
                sum(
                    1
                    for article in articles
                    if article.sentiment
                    == "positive"
                ),

            "negative_count":
                sum(
                    1
                    for article in articles
                    if article.sentiment
                    == "negative"
                ),

            "neutral_count":
                sum(
                    1
                    for article in articles
                    if article.sentiment
                    == "neutral"
                ),
        }
        
    def get_combined_summary(
        self,
        symbol: str,
        limit: int = 20
    ):

        company_news = (
            self.get_recent_summary(
                symbol,
                limit
            )
        )

        market_news = (
            self.get_recent_summary(
                "MARKET",
                limit
            )
        )

        return {

            "avg_news_score":
                (
                    company_news["avg_news_score"]
                    +
                    market_news["avg_news_score"]
                ) / 2,

            "avg_confidence":
                (
                    company_news["avg_confidence"]
                    +
                    market_news["avg_confidence"]
                ) / 2,

            "article_count":
                company_news["article_count"]
                +
                market_news["article_count"],

            "recent_article_count":
                company_news["recent_article_count"]
                +
                market_news["recent_article_count"],

            "positive_count":
                company_news["positive_count"]
                +
                market_news["positive_count"],

            "negative_count":
                company_news["negative_count"]
                +
                market_news["negative_count"],

            "neutral_count":
                company_news["neutral_count"]
                +
                market_news["neutral_count"],
        }

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