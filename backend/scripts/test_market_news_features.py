from database.session import SessionLocal

from repositories.news_article_repository import (
    NewsArticleRepository,
)

db = SessionLocal()

try:

    news = (
        NewsArticleRepository(db)
        .get_recent_summary(
            "MARKET"
        )
    )

    print(news)

finally:
    db.close()