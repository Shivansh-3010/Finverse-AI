from database.session import SessionLocal
from models.news_article import NewsArticle

db = SessionLocal()

articles = (
    db.query(NewsArticle)
    .filter(
        NewsArticle.provider == "historical_dataset"
    )
    .limit(5)
    .all()
)

for article in articles:

    print("=" * 80)

    print("TITLE:")
    print(article.title)

    print("SENTIMENT:")
    print(article.sentiment)

    print("CONFIDENCE:")
    print(article.confidence)

    print("EVENTS:")
    print(article.events)

    print("NEWS SCORE:")
    print(article.news_score)

    print()

db.close()