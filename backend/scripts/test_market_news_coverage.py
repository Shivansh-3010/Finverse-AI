from database.session import SessionLocal
from models.news_article import NewsArticle

db = SessionLocal()

try:

    articles = (
        db.query(NewsArticle)
        .filter(
            NewsArticle.provider
            == "historical_dataset"
        )
        .all()
    )

    dates = {
        article.published_at.date()
        for article in articles
        if article.published_at
    }

    print(
        "Articles:",
        len(articles)
    )

    print(
        "Unique Dates:",
        len(dates)
    )

    print(
        "Earliest:",
        min(dates)
    )

    print(
        "Latest:",
        max(dates)
    )

finally:
    db.close()